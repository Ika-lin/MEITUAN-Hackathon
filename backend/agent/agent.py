"""
Weekendgo product agent.

This version keeps the AI-agent-native experience, but moves product control
from prompt-only behavior into deterministic routing, planning, validation,
and state. LLM calls are used for language polish, not as the only executor.
"""
from __future__ import annotations

import json
import re
from typing import Any

from agent.context_builder import build_context, SYSTEM_PROMPT
from agent.intent_router import route_intent
from agent.llm_client import call_deepseek, parse_json_response
from agent.memory import get_memory
from agent.planning_service import (
    build_places_reply,
    build_plan_reply,
    build_trip_plan,
    find_places,
    save_plan,
)
from agent.profile_service import compact_profile_text, get_structured_profile
from agent.response_schema import agent_response, safe_json_result, tool_log
from agent.tools import execute_tool


PERSONAS = {
    "规划师": {"emoji": "📋", "color": "#4A90D9", "focus": "时间、路线、预算"},
    "美食家": {"emoji": "🍜", "color": "#E8734A", "focus": "口味、口碑、性价比"},
    "本地通": {"emoji": "🗺️", "color": "#3CB371", "focus": "区域、避坑、动线"},
    "文艺青年": {"emoji": "🎨", "color": "#9B59B6", "focus": "氛围、拍照、体验质感"},
}


def agent_chat(
    user_message: str,
    history: list[dict] | None = None,
    user_id: str | None = None,
    state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Single-user product agent entrypoint."""
    history = history or []
    user_id = user_id or "u_demo_001"
    state = state if state is not None else {}
    memory = get_memory()

    # 统一上下文组装
    ctx = build_context(user_message, user_id, history, state)

    # Intent router —— 传历史用于消歧（如"就这个"→确认上轮方案）
    routed = route_intent(user_message, history)
    intent = routed["intent"]
    slots = routed.get("slots", {})

    if intent == "greeting":
        result = _handle_greeting(user_id, ctx)
    elif intent == "confirm_plan":
        result = _handle_confirm(user_id, state)
    elif intent == "onboarding_profile":
        result = _handle_onboarding_profile(user_id, ctx)
    elif intent == "find_place":
        result = _handle_find_place(slots, ctx)
    elif intent == "plan_trip":
        result = _handle_plan_trip(user_id, user_message, slots, ctx, state)
    elif intent == "modify_plan":
        result = _handle_modify_plan(user_id, user_message, slots, ctx, state)
    elif intent == "update_profile":
        result = _handle_update_profile(user_id, user_message, slots)
    else:
        result = _handle_smalltalk(user_message, ctx, state)

    profile = get_structured_profile(user_id)
    result.setdefault("metadata", {})
    result["metadata"].update({
        "router": routed,
        "profile": {
            "userId": profile["userId"],
            "nickname": profile["nickname"],
            "personaTags": profile.get("personaTags", []),
            "avgSpending": profile.get("avgSpending"),
        },
    })

    state.update(result.pop("state_patch", {}))
    memory.sync(user_message, result.get("reply", ""), result.get("tool_calls", []), user_id=user_id)
    return result


def group_chat(user_message: str, history: list[dict] | None = None) -> dict[str, Any]:
    """Persona panel for lightweight group discussion."""
    history = history or []
    routed = route_intent(user_message, history)
    slots = routed.get("slots", {})
    messages = []

    for name, cfg in PERSONAS.items():
        text = _persona_reply(name, cfg["focus"], user_message, slots)
        messages.append({
            "persona": name,
            "emoji": cfg["emoji"],
            "color": cfg["color"],
            "text": text,
        })

    return {
        "messages": messages,
        "trip": None,
        "intent": routed["intent"],
        "actions": [{"type": "group_plan", "label": "发起群规划", "status": "ready"}],
    }


def group_synthesize(history: list[dict]) -> dict[str, Any]:
    """Summarize group chat without depending on tool-calling LLM behavior."""
    recent = " ".join(item.get("content", "") for item in (history or [])[-8:])
    routed = route_intent(recent)
    return {
        "reply": "我已经整理了群里的偏好。现在可以发起群规划，我会读取每个成员画像，统一生成路线和冲突说明。",
        "trip": None,
        "intent": routed["intent"],
        "actions": [{"type": "group_plan", "label": "生成统一方案", "status": "ready"}],
    }


def _handle_greeting(user_id: str, ctx) -> dict[str, Any]:
    """基于最近消费记录生成自然开场白"""
    raw_text = execute_tool("get_user_raw_data", {"user_id": user_id, "limit": 3})
    raw = safe_json_result(raw_text)
    records = raw.get("records", [])
    tool_calls = [tool_log("get_user_raw_data", args={"user_id": user_id, "limit": 3},
                           result={"totalRecords": raw.get("totalRecords", 0)})]

    if not records:
        return agent_response(
            reply="Hi！欢迎来到 Weekendgo ✨ 告诉我你想怎么过周末吧～",
            intent="greeting", stage="done", tool_calls=tool_calls,
            actions=[{"type": "start_plan", "label": "开始规划", "status": "ready"}],
        )

    latest = records[0]
    prompt = (
        "你是 Weekendgo。用户刚打开 App，根据他最近消费记录用朋友语气寒暄一句（15-30字），自然过渡到'这周末想怎么安排'。"
        f"\n{ctx.profile}"
        f"\n最近：{latest['date']} {latest['timeOfDay']} | {latest['poiName']} | {latest['category']} | ¥{latest['amount']}"
        "\n只输出一句话。"
    )
    content, err = call_deepseek(
        [{"role": "user", "content": prompt}],
        temperature=0.8, max_tokens=80, timeout_seconds=10,
    )
    reply = content.strip() if content and not err else (
        f"Hi！上次{latest['date']}去了{latest['poiName']}，感觉怎么样？这周末想怎么安排？"
    )
    return agent_response(
        reply=reply, intent="greeting", stage="done", tool_calls=tool_calls,
        actions=[{"type": "start_plan", "label": "开始规划", "status": "ready"}],
    )


def _handle_find_place(slots: dict, ctx) -> dict[str, Any]:
    profile = ctx.profile_data or get_structured_profile(ctx.user_id)
    places, tool_calls = find_places(slots, profile)
    reply = build_places_reply(places, slots)
    return agent_response(
        reply=reply, intent="find_place", stage="suggesting",
        tool_calls=tool_calls, suggestions=places,
        actions=[{"type": "plan_from_places", "label": "安排成路线", "status": "ready"}],
    )


def _handle_onboarding_profile(user_id: str, ctx) -> dict[str, Any]:
    profile = get_structured_profile(user_id)
    analysis, tool_calls, analysis_meta = _analyze_onboarding_profile(user_id, profile)
    reply = _format_onboarding_analysis(analysis) if analysis else _fallback_onboarding_summary(profile)
    return agent_response(
        reply=reply, intent="onboarding_profile", stage="profile_ready",
        tool_calls=tool_calls,
        actions=[{"type": "start_using", "label": "开始使用", "status": "ready"}],
        metadata={"onboarding": True, "agentAnalyzed": bool(analysis)},
    )


def _analyze_onboarding_profile(
    user_id: str,
    profile: dict[str, Any],
) -> tuple[dict[str, Any] | None, list[dict[str, Any]], dict[str, Any]]:
    raw_text = execute_tool("get_user_raw_data", {"user_id": user_id, "limit": 40})
    raw_data = safe_json_result(raw_text)
    records = raw_data.get("records", [])[:28]
    tool_calls = [tool_log(
        "get_user_raw_data",
        args={"user_id": user_id, "limit": 40},
        result={
            "totalRecords": raw_data.get("totalRecords", len(records)),
            "usedRecords": len(records),
            "dataSource": raw_data.get("dataSource", ""),
        },
    )]

    prompt = f"""
你是 Weekendgo 的用户理解 Agent。现在是首次登录 onboarding，只做画像分析，不生成任何行程、路线、站点安排或时间表。

请基于下面的模拟美团生态原始记录，自己分析用户偏好。注意：
- source=search 只能表示兴趣，不代表真实消费或到店。
- source=bike 只能表示出行/活动半径，不代表消费偏好。
- amount=0 不参与消费水平判断。
- delivery 代表口味偏好，但不代表线下常去地点。
- 输出必须是 JSON，不要 Markdown。

用户基础画像（可作为弱参考，不能替代原始记录分析）：
{json.dumps(profile, ensure_ascii=False)}

原始记录：
{json.dumps(records, ensure_ascii=False)}

JSON 格式：
{{
  "greeting": "一句温暖的开场，不超过30字",
  "summary": "你对这个用户的整体理解，不超过80字",
  "evidence": ["2-4条基于原始记录的证据"],
  "preferences": {{
    "categories": ["偏好的活动/消费类型"],
    "areas": ["常活动区域"],
    "budget": "消费水平判断",
    "socialStyle": "独处/社交/均衡等判断",
    "timeStyle": "常见活动时间判断"
  }},
  "interestSignals": ["搜索/浏览等弱兴趣信号，若没有则空数组"],
  "nextPrompt": "引导用户开始使用的一句话，不要替用户规划"
}}
"""
    content, err = call_deepseek(
        [{"role": "user", "content": prompt}],
        temperature=0.35,
        max_tokens=900,
        response_format={"type": "json_object"},
        timeout_seconds=18,
    )
    if err or not content:
        return None, tool_calls, {"status": "failed", "reason": err or "empty_content"}

    parsed, parse_err = parse_json_response(content)
    if parse_err or not isinstance(parsed, dict):
        return None, tool_calls, {"status": "rejected", "reason": parse_err or "invalid_json"}

    validation_error = _validate_onboarding_analysis(parsed)
    if validation_error:
        return None, tool_calls, {"status": "rejected", "reason": validation_error}

    return parsed, tool_calls, {"status": "success", "reason": ""}


def _validate_onboarding_analysis(analysis: dict[str, Any]) -> str | None:
    text = json.dumps(analysis, ensure_ascii=False)
    blocked_words = ["第1站", "第2站", "路线", "行程安排", "14:00", "15:00", "保存行程"]
    if any(word in text for word in blocked_words):
        return "contains_trip_plan"
    if not analysis.get("summary"):
        return "missing_summary"
    if len(text) > 1400:
        return "too_long"
    return None


def _format_onboarding_analysis(analysis: dict[str, Any]) -> str:
    lines = [
        analysis.get("greeting") or "我大概了解你了。",
        analysis.get("summary", ""),
    ]
    evidence = analysis.get("evidence") or []
    if evidence:
        lines.append("我主要看到了这些信号：")
        lines.extend(f"- {item}" for item in evidence[:4])

    prefs = analysis.get("preferences") or {}
    pref_bits = []
    if prefs.get("categories"):
        pref_bits.append("偏好：" + "、".join(prefs["categories"][:4]))
    if prefs.get("areas"):
        pref_bits.append("常活动：" + "、".join(prefs["areas"][:3]))
    if prefs.get("budget"):
        pref_bits.append("消费：" + str(prefs["budget"]))
    if prefs.get("socialStyle"):
        pref_bits.append("节奏：" + str(prefs["socialStyle"]))
    if pref_bits:
        lines.append("；".join(pref_bits))

    interests = analysis.get("interestSignals") or []
    if interests:
        lines.append("另外，我会把这些当作兴趣信号，而不是已消费偏好：" + "、".join(interests[:3]))

    lines.append(analysis.get("nextPrompt") or "接下来告诉我时间、人数、预算或心情，我再开始帮你规划。")
    return "\n\n".join(line for line in lines if line)


def _fallback_onboarding_summary(profile: dict[str, Any]) -> str:
    categories = "、".join(
        item.get("category", "") for item in (profile.get("favoriteCategories") or [])[:3]
        if item.get("category")
    ) or "本地生活"
    areas = "、".join(
        item.get("district", "") for item in (profile.get("favoriteDistricts") or [])[:3]
        if item.get("district")
    ) or profile.get("location", "上海")
    tags = "、".join((profile.get("personaTags") or profile.get("favoriteTags") or [])[:4])
    interest = "、".join(
        item.get("category", "") for item in (profile.get("interestCategories") or [])[:2]
        if item.get("category")
    )

    lines = [
        f"我大概了解你了，{profile.get('nickname', '朋友')}。",
        f"你平时更偏向 {categories}，常活动在 {areas}，舒适消费大概在人均 {int(profile.get('avgSpending') or 0)} 元左右。",
    ]
    if tags:
        lines.append(f"你的生活关键词像是：{tags}。")
    if interest:
        lines.append(f"我也注意到你最近对 {interest} 有兴趣，但会把它当作兴趣信号，而不是已消费偏好。")
    if profile.get("personaSummary"):
        lines.append(profile["personaSummary"])
    lines.append("接下来你只要告诉我时间、人数、预算或心情，我再开始帮你规划。")
    return "\n\n".join(lines)


def _handle_plan_trip(
    user_id: str, message: str, slots: dict, ctx, state: dict[str, Any],
) -> dict[str, Any]:
    profile = ctx.profile_data or get_structured_profile(user_id)
    plan, tool_calls = build_trip_plan(user_id, message, slots, profile)
    base_reply = build_plan_reply(plan, profile)
    if ctx.memory:
        base_reply = f"[回忆] {ctx.memory}\n\n{base_reply}"
    reply, polish_meta = _polish_reply(base_reply, plan, profile)

    state_patch = {"last_plan": plan}
    return agent_response(
        reply=reply,
        intent="plan_trip",
        stage="draft_plan",
        tool_calls=tool_calls,
        trip=plan,
        actions=[
            {"type": "save_trip", "label": "保存行程", "status": "ready"},
            {"type": "modify_trip", "label": "调整路线", "status": "ready"},
        ],
        needs=plan.get("needs", []),
        state_patch=state_patch,
        metadata={"llmPolish": polish_meta},
    )


def _handle_modify_plan(
    user_id: str, message: str, slots: dict, ctx, state: dict[str, Any],
) -> dict[str, Any]:
    profile = ctx.profile_data or get_structured_profile(user_id)
    previous = state.get("last_plan")
    merged_slots = dict((previous or {}).get("slots", {}))
    merged_slots.update(slots)
    plan, tool_calls = build_trip_plan(user_id, message, merged_slots, profile)
    reply = "我按你的新要求重新调整了一版。\n\n" + build_plan_reply(plan, profile)
    return agent_response(
        reply=reply,
        intent="modify_plan",
        stage="draft_plan",
        tool_calls=tool_calls,
        trip=plan,
        actions=[
            {"type": "save_trip", "label": "保存新版", "status": "ready"},
            {"type": "modify_trip", "label": "继续调整", "status": "ready"},
        ],
        state_patch={"last_plan": plan},
    )


def _handle_confirm(user_id: str, state: dict[str, Any]) -> dict[str, Any]:
    last_plan = state.get("last_plan")
    saved_trip, tool_calls = save_plan(user_id, last_plan)
    if not saved_trip:
        return agent_response(
            reply="我还没有可保存的行程草稿。你先告诉我时间、预算和想玩的类型，我来生成一版。",
            intent="confirm_plan",
            stage="needs_plan",
            tool_calls=tool_calls,
            needs=["plan"],
        )

    # 一键执行：预订餐厅 + 买门票（用 last_plan 的 stops，有完整 category/poiId）
    exec_actions = []
    plan_stops = (last_plan or {}).get("stops", [])
    for stop in plan_stops[:4]:
        if stop.get("category") == "美食":
            exec_actions.append({
                "type": "reserve_restaurant",
                "poi_name": stop.get("name", ""),
                "poi_id": stop.get("poiId", ""),
                "time": stop.get("time", "18:00"),
                "party_size": 2,
            })
        if stop.get("category") in ("艺术", "展览"):
            exec_actions.append({
                "type": "buy_tickets",
                "poi_name": stop.get("name", ""),
                "poi_id": stop.get("poiId", ""),
                "count": 2,
            })

    exec_raw = execute_tool("execute_actions", {"actions": exec_actions}) if exec_actions else None
    exec_result = safe_json_result(exec_raw) if exec_raw else {}
    if exec_result.get("success"):
        tool_calls.append(tool_log("execute_actions", args={"actions": exec_actions}, result=exec_result))
    share_msg = exec_result.get("shareMessage", "")

    reply = f"已保存「{saved_trip.get('title', '周末出行')}」。"
    if exec_actions:
        reply += "\n\n已一键安排好：\n" + "\n".join(f"✅ {r.get('detail','')}" for r in exec_result.get("results", []))
        if share_msg:
            reply += f"\n\n📤 可以发给朋友：\n{share_msg}"
    reply += "\n\n你可以在行程页继续查看、替换站点或打卡。"

    return agent_response(
        reply=reply,
        intent="confirm_plan",
        stage="saved_and_executed",
        tool_calls=tool_calls,
        trip=saved_trip,
        actions=[
            {"type": "open_trip", "label": "查看行程", "status": "ready"},
            {"type": "modify_trip", "label": "调整路线", "status": "ready"},
        ],
        state_patch={"last_trip": saved_trip, "last_plan": None},
    )


def _handle_update_profile(user_id: str, message: str, slots: dict) -> dict[str, Any]:
    args: dict[str, Any] = {"user_id": user_id, "notes": message}
    if slots.get("budget"):
        args["budget_comfort"] = int(slots["budget"]) if isinstance(slots["budget"], (int, str)) and str(slots["budget"]).isdigit() else args.get("budget_comfort", 0)
    if slots.get("dietary"):
        args["dietary"] = slots["dietary"]
    if slots.get("mobility"):
        args["mobility"] = slots["mobility"]
    if slots.get("areas"):
        args["preferred_areas"] = slots["areas"]
    # 从自然语言中提取习惯
    import re as _re
    m = _re.search(r'(\d+)[:：点]?\s*(下班|到家)', message)
    if m:
        args["off_work_time"] = f"{m.group(1)}:00"
    m2 = _re.search(r'通勤[大约要]?\s*(\d+)\s*(分钟|分)', message)
    if m2:
        args["commute_minutes"] = int(m2.group(1))
    if '周六' in message or '星期天' in message:
        slots_list = []
        if '周六' in message: slots_list.append('周六')
        if '周日' in message or '星期天' in message: slots_list.append('周日')
        if '下午' in message: slots_list = [s+'下午' for s in slots_list] if slots_list else ['下午']
        if slots_list:
            args["free_slots"] = slots_list
    # 家/公司位置
    home_m = _re.search(r'(?:住在|家住|家在)\s*([一-鿿]{2,4})', message)
    if home_m:
        args["home_area"] = home_m.group(1)
    work_m = _re.search(r'公司在\s*([一-鿿]{2,4})', message)
    if work_m:
        args["work_area"] = work_m.group(1)

    raw = execute_tool("update_user_habits", args)
    result = safe_json_result(raw)
    changed = "、".join(result.get("updatedFields", [])) or "偏好备注"
    return agent_response(
        reply=f"记住了，我已经更新你的{changed}。后面推荐会优先参考这些偏好。",
        intent="update_profile",
        stage="saved",
        tool_calls=[tool_log("update_user_habits", args=args, result=result)],
        metadata={"updatedProfile": result.get("profile")},
    )


def _handle_smalltalk(user_message: str, ctx, state: dict = None) -> dict[str, Any]:
    state = state or {}

    # 检测是否想和朋友一起
    group_keywords = ["朋友", "一起", "大家", "几个人", "组队", "组局", "约", "搭子", "群"]
    wants_group = any(w in user_message for w in group_keywords)
    actions = [{"type": "start_plan", "label": "开始规划", "status": "ready"}]
    if wants_group:
        actions.append({"type": "create_group", "label": "建群一起规划", "status": "ready"})

    # 主动了解习惯
    profile = ctx.profile_data or get_structured_profile(ctx.user_id)
    asked = state.get("asked_habit_questions", [])
    habit_q = _pick_habit_question(profile, asked)
    if habit_q:
        asked.append(habit_q["key"])
        habit_hint = f"\n回复末尾自然加一句：「{habit_q['question']}」用'对了'、'说起来'引入。"
    else:
        habit_hint = ""

    # 用 ContextBlock 组装完整 prompt（含 history）
    prompt = ctx.build(with_history=True)
    if habit_hint:
        prompt += f"\n{habit_hint}"
    prompt += "\n请用简短自然的中文回复，引导用户给出时间、预算或偏好。"

    content, err = call_deepseek(
        [{"role": "user", "content": prompt}],
        temperature=0.7, max_tokens=400, timeout_seconds=20,
    )
    reply = content if content and not err else (
        "我在。告诉我什么时候、几个人、预算多少、偏好哪种类型，我来安排。"
    )
    return agent_response(
        reply=reply, intent="smalltalk", stage="chatting",
        actions=actions, state_patch={"asked_habit_questions": asked},
    )


# 画像缺口 → 自然问题
HABIT_QUESTIONS = [
    {"key": "home_area", "check": lambda p: not p.get("homeArea"),
     "question": "对了，你住哪个区？这样我能优先推荐离家近的地方"},
    {"key": "work_area", "check": lambda p: not p.get("workArea"),
     "question": "说起来，你公司在哪个区？工作日午餐外卖也能看出你的口味"},
    {"key": "off_work", "check": lambda p: not p.get("offWorkTime"),
     "question": "平时一般几点下班？工作日晚上能不能安排活动就看这个了"},
    {"key": "commute", "check": lambda p: not p.get("commuteMinutes"),
     "question": "通勤大概多久？周末不想跑太远我就帮你圈个范围"},
    {"key": "free_slots", "check": lambda p: not (p.get("freeSlots") or p.get("preferredTime")),
     "question": "周末哪天比较空？周六还是周日？上午还是下午出门？"},
    {"key": "dietary", "check": lambda p: not p.get("dietary"),
     "question": "饮食上有什么偏好吗？不吃辣、在减肥、或者有什么忌口？"},
    {"key": "mobility", "check": lambda p: not p.get("mobility"),
     "question": "出门喜欢走路逛还是坐地铁？或者开车？"},
    {"key": "budget", "check": lambda p: not p.get("budgetComfort") and not p.get("avgSpending"),
     "question": "周末出门一般预算多少？我推荐的时候帮你控制"},
]

def _pick_habit_question(profile: dict, asked: list[str]) -> dict | None:
    for q in HABIT_QUESTIONS:
        if q["key"] not in asked and q["check"](profile):
            return q
    return None


def _polish_reply(base_reply: str, plan: dict[str, Any], profile: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    if not plan.get("stops"):
        return base_reply, {"status": "skipped", "reason": "no_stops"}

    prompt = (
        "你是 Weekendgo 的表达层。下面已经有系统生成好的结构化行程，"
        "请只润色表达，不要新增地点、价格、时间或不存在的数据。"
        f"\n用户画像：{compact_profile_text(profile)}"
        f"\n结构化行程：{json.dumps(plan, ensure_ascii=False)}"
        f"\n基础文案：{base_reply}"
        "\n输出 260 字以内，保留站点时间和保存/调整提示。"
    )
    content, err = call_deepseek(
        [{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=520,
        timeout_seconds=12,
    )
    if err or not content:
        return base_reply, {"status": "failed", "reason": err or "empty_content"}

    polished = content.strip()
    validation_error = _validate_polished_reply(polished, plan)
    if validation_error:
        return base_reply, {"status": "rejected", "reason": validation_error}

    return polished, {"status": "success", "reason": ""}


def _validate_polished_reply(reply: str, plan: dict[str, Any]) -> str | None:
    if len(reply) > 520:
        return "too_long"

    stops = plan.get("stops", [])
    stop_names = [s.get("name", "") for s in stops if s.get("name")]
    if stop_names and not any(name in reply for name in stop_names):
        return "missing_planned_places"

    allowed_times = set()
    for stop in stops:
        if stop.get("time"):
            allowed_times.add(stop["time"])
        if stop.get("endTime"):
            allowed_times.add(stop["endTime"])
    mentioned_times = set(re.findall(r"\b(?:[01]?\d|2[0-3]):[0-5]\d\b", reply))
    if mentioned_times - allowed_times:
        return "introduced_unplanned_time"

    allowed_amounts = {str(s.get("pricePerCapita")) for s in stops if s.get("pricePerCapita") is not None}
    if plan.get("budgetValue") is not None:
        allowed_amounts.add(str(plan["budgetValue"]))
    mentioned_amounts = set(re.findall(r"(?:¥|人均约?|约)\s*(\d{2,5})", reply))
    if mentioned_amounts - allowed_amounts:
        return "introduced_unplanned_price"

    return None


def _persona_reply(name: str, focus: str, message: str, slots: dict) -> str:
    category = slots.get("category") or "活动"
    area = slots.get("area") or "顺路区域"
    if name == "规划师":
        return f"我会先把时间、预算和动线压住，优先在{area}内安排 2-4 站，避免来回跑。"
    if name == "美食家":
        return f"如果这次包含{category}，我会优先选评分高、预算稳、周末不太踩雷的店。"
    if name == "本地通":
        return f"路线最好围绕一个街区展开，{area}这种连续步行体验会比跨区舒服。"
    return "氛围上建议留一站慢节奏空间，方便拍照、聊天，也让行程不只是赶场。"

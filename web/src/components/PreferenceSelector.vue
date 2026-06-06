<script setup lang="ts">
import { ref } from 'vue'

// Image constants from Figma
const imgGroup2 = 'https://www.figma.com/api/mcp/asset/2eac2554-c84d-4605-988d-f0d15e8e30d3'
const imgIcon = 'https://www.figma.com/api/mcp/asset/284e597d-d983-4a81-bba0-add236d3e2d2'
const imgVector = 'https://www.figma.com/api/mcp/asset/bbdd6747-d5b8-4f79-a6a1-a947c20cbc8b'
const imgGroup40 = 'https://www.figma.com/api/mcp/asset/8664e61c-a452-4392-bd80-05b644298240'
const imgVector1 = 'https://www.figma.com/api/mcp/asset/8dae70e2-6420-4cb5-be71-75503366954c'
const imgVector2 = 'https://www.figma.com/api/mcp/asset/65b641de-c8d3-4c83-95bf-db717a0d107b'
const imgVector3 = 'https://www.figma.com/api/mcp/asset/2a2e3099-9559-444b-a203-d83331fd019a'
const imgVector4 = 'https://www.figma.com/api/mcp/asset/511f50c1-23a8-4efc-8b78-62b75fb17682'
const imgVector5 = 'https://www.figma.com/api/mcp/asset/7b2670e7-9fff-40e2-8ea5-dc5a92cedcf2'
const imgVector6 = 'https://www.figma.com/api/mcp/asset/c7c5bfa6-ece4-4c58-8d53-6eee9bb8b0aa'
const imgLine1 = 'https://www.figma.com/api/mcp/asset/ba915d5a-7041-400c-84cb-dd2268236545'
const imgEllipse1 = 'https://www.figma.com/api/mcp/asset/9b650293-f7a9-4eb9-a0aa-1a166932f90e'
const imgLine3 = 'https://www.figma.com/api/mcp/asset/c13a58b5-e380-4744-812a-560c97671f4c'
const imgIconParkOutlineLeft = 'https://www.figma.com/api/mcp/asset/4611f36a-f10f-4f21-b572-7bcc4d5ccd5b'
const imgLevels = 'https://www.figma.com/api/mcp/asset/1f6d5e15-307d-4f0c-bd28-88e3bb132da2'

// State management
const selectedTimeType = ref<'short' | 'city' | 'weekend'>('short')
const selectedActivities = ref<string[]>([])
const selectedRange = ref<'near' | 'metro' | 'cross'>('near')
const selectedBudget = ref<'100' | '200' | '300' | 'unlimited'>('100')
const timelineValue = ref(0)

const activities = [
  { id: 'food', label: '寻味美食', icon: imgVector },
  { id: 'coffee', label: '喝咖啡', icon: imgVector1 },
  { id: 'street', label: '逛街区', icon: imgVector2 },
  { id: 'walk', label: '城市散步', icon: imgVector3 },
  { id: 'bookstore', label: '书店阅读', icon: imgVector4 },
  { id: 'exhibition', label: '看展览', icon: imgVector5 },
  { id: 'photo', label: '拍照打卡', icon: imgVector6 },
  { id: 'craft', label: '手作体验', icon: imgGroup40 }
]

const toggleActivity = (id: string) => {
  const index = selectedActivities.value.indexOf(id)
  if (index > -1) {
    selectedActivities.value.splice(index, 1)
  } else {
    selectedActivities.value.push(id)
  }
}

const generatePlan = () => {
  const preferences = {
    timeType: selectedTimeType.value,
    activities: selectedActivities.value,
    range: selectedRange.value,
    budget: selectedBudget.value,
    timeline: timelineValue.value
  }
  console.log('Generated preferences:', preferences)
  // TODO: Emit event or call API with preferences
}

const goBack = () => {
  // TODO: Implement navigation
}
</script>

<template>
  <div class="relative w-full h-full bg-[#f9f9f9] rounded-[40px] overflow-hidden" style="font-family: 'FZLanTingHeiS-DB-GB', sans-serif">
    <!-- Background decoration -->
    <div class="absolute -left-[127px] -top-[58px] w-[606.807px] h-[934px]">
      <img :src="imgGroup2" alt="decoration" class="w-full h-full object-cover" />
    </div>

    <!-- Status Bar -->
    <div class="absolute top-0 left-0 w-full h-[54px] flex items-center justify-between px-4">
      <div class="text-[17px] font-semibold text-black">9:41</div>
      <div class="bg-[#2a2a2a] h-[28px] rounded-full w-[104px]"></div>
      <img :src="imgLevels" alt="signal" class="h-[54px]" />
    </div>

    <!-- Back Button -->
    <button
      @click="goBack"
      class="absolute top-[62px] left-[11px] w-[40px] h-[40px] rounded-full bg-white border border-[#f3f3f3] flex items-center justify-center"
    >
      <img :src="imgIconParkOutlineLeft" alt="back" class="w-4 h-4" />
    </button>

    <!-- Skip Button -->
    <div class="absolute top-[61px] right-[309px] flex items-center justify-center">
      <div class="bg-white h-[40px] rounded-[75.65px] w-[63px] flex items-center justify-center">
        <span class="text-[13px] text-black font-normal">跳过</span>
      </div>
    </div>

    <!-- Title -->
    <div class="absolute top-[96px] left-1/2 -translate-x-1/2 text-center">
      <p class="text-[19.643px] text-[#1b1c1c] font-normal leading-[22px]">告诉我你的偏好</p>
    </div>

    <!-- Section: Time Type Selection -->
    <div class="absolute top-[159px] left-[17px]">
      <p class="text-[15px] text-[#5c5c5c] font-normal mb-4">游玩时间类型</p>
      
      <div class="flex gap-4 absolute top-[196px]">
        <button
          @click="selectedTimeType = 'short'"
          :class="[
            'w-[114px] h-[48px] rounded-[41px] border-2 font-normal text-[11px] flex items-center justify-center',
            selectedTimeType === 'short'
              ? 'bg-[#e8e3e7] border-[#461c3a]'
              : 'bg-white border-[#b4b4b4]'
          ]"
        >
          短时闲逛
        </button>
        <button
          @click="selectedTimeType = 'city'"
          :class="[
            'w-[112px] h-[48px] rounded-[41px] border-2 font-normal text-[11px] flex items-center justify-center',
            selectedTimeType === 'city'
              ? 'bg-[#e8e3e7] border-[#461c3a]'
              : 'bg-white border-[#b4b4b4]'
          ]"
        >
          城市一日
        </button>
        <button
          @click="selectedTimeType = 'weekend'"
          :class="[
            'w-[114px] h-[48px] rounded-[41px] border-2 font-normal text-[11px] flex items-center justify-center',
            selectedTimeType === 'weekend'
              ? 'bg-[#e8e3e7] border-[#461c3a]'
              : 'bg-white border-[#b4b4b4]'
          ]"
        >
          周末两天
        </button>
      </div>
    </div>

    <!-- Timeline Selection - Only show for 'short' time type -->
    <div v-if="selectedTimeType === 'short'" class="absolute top-[256px] left-1/2 -translate-x-1/2 w-[360px]">
      <div class="bg-[rgba(255,255,255,0.8)] border border-[#d8d8d8] rounded-[9.778px] p-4">
        <p class="text-[11px] text-black font-normal mb-2">预计可用时间</p>
        
        <div class="flex items-center justify-between">
          <span class="text-[10px] text-[#919191]">1小时</span>
          
          <input
            v-model.number="timelineValue"
            type="range"
            min="0"
            max="5"
            class="mx-4 flex-1"
            style="height: 2px; background: linear-gradient(to right, #b4b4b4 0%, #b4b4b4 100%)"
          />
          
          <span class="text-[10px] text-[#919191]">6小时</span>
        </div>
        
        <div class="mt-2 text-right text-[10px] text-black">{{ timelineValue }}小时</div>
      </div>
    </div>

    <!-- Section: Activities Selection -->
    <div class="absolute top-[350px] left-[17px]">
      <p class="text-[15px] text-[#5c5c5c] font-normal mb-4">活动偏好 (多选)</p>
      
      <div class="absolute top-[391px] flex flex-wrap gap-3 w-[360px]">
        <button
          v-for="activity in activities.slice(0, 4)"
          :key="activity.id"
          @click="toggleActivity(activity.id)"
          :class="[
            'h-[42px] rounded-[100px] border-[1.03px] border-solid flex items-center justify-center gap-2 text-[11px] font-normal',
            selectedActivities.includes(activity.id)
              ? 'bg-[#e8e3e7] border-[#461c3a]'
              : 'bg-white border-[#b4b4b4]'
          ]"
        >
          <img :src="activity.icon" :alt="activity.label" class="w-4 h-4" />
          <span>{{ activity.label }}</span>
        </button>
      </div>

      <div class="absolute top-[446px] flex flex-wrap gap-3 w-[360px]">
        <button
          v-for="activity in activities.slice(4, 8)"
          :key="activity.id"
          @click="toggleActivity(activity.id)"
          :class="[
            'h-[42px] rounded-[27px] border-[1.03px] border-solid flex items-center justify-center gap-2 text-[11px] font-normal',
            selectedActivities.includes(activity.id)
              ? 'bg-[#e8e3e7] border-[#461c3a]'
              : 'bg-white border-[#b4b4b4]'
          ]"
        >
          <img :src="activity.icon" :alt="activity.label" class="w-4 h-4" />
          <span>{{ activity.label }}</span>
        </button>
      </div>
    </div>

    <!-- Section: Range Selection -->
    <div class="absolute top-[519px] left-[17px]">
      <p class="text-[15px] text-[#5c5c5c] font-normal mb-4">出行范围</p>
      
      <div class="absolute top-[554px] flex gap-4">
        <button
          @click="selectedRange = 'near'"
          :class="[
            'w-[114px] h-[48px] rounded-[41px] border-2 font-normal text-[11px] flex items-center justify-center',
            selectedRange === 'near'
              ? 'bg-[#e8e3e7] border-[#461c3a]'
              : 'bg-white border-[#b4b4b4]'
          ]"
        >
          就近玩玩
        </button>
        <button
          @click="selectedRange = 'metro'"
          :class="[
            'w-[112px] h-[48px] rounded-[41px] border-2 font-normal text-[11px] flex items-center justify-center',
            selectedRange === 'metro'
              ? 'bg-[#e8e3e7] border-[#461c3a]'
              : 'bg-white border-[#b4b4b4]'
          ]"
        >
          地铁30分钟
        </button>
        <button
          @click="selectedRange = 'cross'"
          :class="[
            'w-[114px] h-[48px] rounded-[41px] border-2 font-normal text-[11px] flex items-center justify-center',
            selectedRange === 'cross'
              ? 'bg-[#e8e3e7] border-[#461c3a]'
              : 'bg-white border-[#b4b4b4]'
          ]"
        >
          可以跨区
        </button>
      </div>
    </div>

    <!-- Section: Budget Selection -->
    <div class="absolute top-[627px] left-[17px]">
      <p class="text-[15px] text-[#5c5c5c] font-normal mb-4">人均预算</p>
      
      <div class="absolute top-[661px] flex gap-3">
        <button
          @click="selectedBudget = '100'"
          :class="[
            'h-[42px] rounded-[27px] border-[1.03px] border-solid flex items-center justify-center px-3 text-[11px] font-normal',
            selectedBudget === '100'
              ? 'bg-[#e8e3e7] border-[#461c3a]'
              : 'bg-white border-[#b4b4b4]'
          ]"
        >
          100元内
        </button>
        <button
          @click="selectedBudget = '200'"
          :class="[
            'h-[42px] rounded-[27px] border-[1.03px] border-solid flex items-center justify-center px-3 text-[11px] font-normal',
            selectedBudget === '200'
              ? 'bg-[#e8e3e7] border-[#461c3a]'
              : 'bg-white border-[#b4b4b4]'
          ]"
        >
          100-200元
        </button>
        <button
          @click="selectedBudget = '300'"
          :class="[
            'h-[42px] rounded-[27px] border-[1.03px] border-solid flex items-center justify-center px-3 text-[11px] font-normal',
            selectedBudget === '300'
              ? 'bg-[#e8e3e7] border-[#461c3a]'
              : 'bg-white border-[#b4b4b4]'
          ]"
        >
          200–300元
        </button>
        <button
          @click="selectedBudget = 'unlimited'"
          :class="[
            'h-[42px] rounded-[27px] border-[1.03px] border-solid flex items-center justify-center px-3 text-[11px] font-normal',
            selectedBudget === 'unlimited'
              ? 'bg-[#e8e3e7] border-[#461c3a]'
              : 'bg-white border-[#b4b4b4]'
          ]"
        >
          不限
        </button>
      </div>
    </div>

    <!-- Generate Plan Button -->
    <button
      @click="generatePlan"
      class="absolute bottom-[54px] left-1/2 -translate-x-1/2 w-[360px] h-[50px] bg-[rgba(255,255,255,0.52)] rounded-[9999px] shadow-[1px_1px_4px_0px_rgba(0,0,0,0.25)] flex items-center justify-center gap-2"
    >
      <span class="text-[20px] text-black font-normal">生成我的闲时计划</span>
      <img :src="imgIcon" alt="generate" class="w-3 h-4" />
    </button>

    <!-- Home Indicator -->
    <div class="absolute bottom-0 left-0 w-full h-[8px] flex items-center justify-center pb-2">
      <div class="bg-[#2a2a2a] h-[5px] rounded-[100px] w-[144px]"></div>
    </div>
  </div>
</template>

<style scoped>
/* Ensure the component fills its container */
:deep(.component-root) {
  width: 100%;
  height: 100%;
}

/* Smooth transitions for button states */
button {
  transition: all 0.3s ease;
}

button:active {
  transform: scale(0.95);
}

/* Timeline slider styling */
input[type='range'] {
  appearance: none;
  -webkit-appearance: none;
  width: 100%;
  height: 2px;
  border-radius: 5px;
  background: linear-gradient(to right, #b4b4b4 0%, #b4b4b4 100%);
  outline: none;
  cursor: pointer;
}

input[type='range']::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #461c3a;
  cursor: pointer;
}

input[type='range']::-moz-range-thumb {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #461c3a;
  cursor: pointer;
  border: none;
}
</style>

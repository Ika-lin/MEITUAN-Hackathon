/**
 * Weekendgo API 服务
 */
const API_BASE = '/api/v1'

export interface ApiEnvelope<T> {
  code: number
  message: string
  data: T
  requestId?: string
  timestamp?: string
}

export interface AgentAction {
  type: string
  label: string
  status?: string
}

export interface ChatPayload {
  reply: string
  intent: string
  stage: string
  toolCalls: any[]
  trip: any | null
  suggestions: any[]
  actions: AgentAction[]
  needs: string[]
  metadata: Record<string, any>
  sessionId: string
  userId: string
}

export interface GroupPayload {
  reply?: string
  messages?: Array<{ persona: string; emoji?: string; color?: string; text: string }>
  trip?: any
  intent?: string
  actions?: AgentAction[]
  sessionId?: string
  mode?: string
}

interface PlanGenerateRequest {
  timeType: string
  activities: string[]
  geographicRange: string
  budget: string
  prompt?: string
  city?: string
}

interface Plan {
  planId: string
  type: string
  title: string
  duration: string
  budgetText: string
  tag: string
  color: string
  score: number
  description: string
  spots: Spot[]
}

interface Spot {
  spotId: string
  name: string
  category: string
  address: string
  etaMinutes: number
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  const json = await res.json()
  if (json.code !== 0) {
    throw new Error(json.message || 'API Error')
  }
  return json.data as T
}

export async function chatAgent(params: {
  message: string
  sessionId: string
  userId: string
  action?: 'onboarding_profile' | string
}): Promise<ChatPayload> {
  return request<ChatPayload>('/chat', {
    method: 'POST',
    body: JSON.stringify(params),
  })
}

export async function resetChat(params: { sessionId: string; userId?: string }): Promise<void> {
  await request('/chat/reset', {
    method: 'POST',
    body: JSON.stringify(params),
  })
}

export async function groupChat(params: {
  message: string
  sessionId: string
  action?: 'chat' | 'synthesize'
}): Promise<GroupPayload> {
  return request<GroupPayload>('/group-chat', {
    method: 'POST',
    body: JSON.stringify(params),
  })
}

export async function groupPlan(params: {
  user_ids: string[]
  message: string
  sessionId: string
}): Promise<GroupPayload> {
  return request<GroupPayload>('/group-chat/plan', {
    method: 'POST',
    body: JSON.stringify(params),
  })
}

export async function generatePlans(params: PlanGenerateRequest): Promise<Plan[]> {
  const data = await request<{ plans: Plan[] }>('/plan/generate', {
    method: 'POST',
    body: JSON.stringify(params),
  })
  return data.plans || []
}

export async function createTrip(params: {
  userId: string
  planId: string
  plan: Plan | any
  date?: string
  city?: string
}): Promise<{ tripId: string; trip: any }> {
  return request('/trip/create', {
    method: 'POST',
    body: JSON.stringify(params),
  })
}

export async function getTripDetail(tripId: string): Promise<any> {
  return request(`/trip/${tripId}`)
}

export async function getTripReminders(tripId: string): Promise<any> {
  return request(`/trip/${tripId}/reminders`)
}

export async function getTripRouteMap(tripId: string): Promise<any> {
  return request(`/trip/${tripId}/route-map`)
}

export async function getTripWeather(tripId: string): Promise<any> {
  return request(`/trip/${tripId}/weather`)
}

export async function getTrips(userId: string): Promise<{ userId: string; items: any[] }> {
  return request(`/trips?userId=${userId}`)
}

export async function adjustTrip(tripId: string, mode: string): Promise<any> {
  return request(`/trip/${tripId}/adjust`, {
    method: 'POST',
    body: JSON.stringify({ mode }),
  })
}

export async function getTripAlternatives(tripId: string, stopId: string): Promise<any> {
  return request(`/trip/${tripId}/stops/${stopId}/alternatives`)
}

export async function replaceTripStop(tripId: string, stopId: string, candidateId: string): Promise<any> {
  return request(`/trip/${tripId}/stops/${stopId}/replace`, {
    method: 'POST',
    body: JSON.stringify({ candidateId }),
  })
}

export async function getPoiDetail(poiId: string): Promise<any> {
  return request(`/pois/${poiId}`)
}

export async function getDiscoverCategories(): Promise<{ categories: string[] }> {
  return request('/discover/categories')
}

export async function getDiscoverPlaces(category?: string): Promise<{ items: any[] }> {
  const params = category && category !== '全部' ? `?category=${category}` : ''
  return request(`/discover/places${params}`)
}

export async function getDiscoverEvents(): Promise<{ events: any[] }> {
  return request('/discover/events')
}

export async function getUserProfile(userId: string = 'u_demo_001'): Promise<any> {
  return request(`/user/profile?userId=${userId}`)
}

export async function getUserFootprints(userId: string): Promise<{ userId: string; total: number; footprints: any[] }> {
  return request(`/user/${userId}/footprints`)
}

export type { Plan, Spot, PlanGenerateRequest }

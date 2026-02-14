import axios from 'axios'

// Force API URL - ensure it's pointing to backend
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Log the API URL being used
console.log('[API Config] Using API URL:', API_URL)

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor to log API calls
api.interceptors.request.use(
  (config) => {
    const fullUrl = (config.baseURL || '') + (config.url || '')
    console.log('[API] Making request to:', fullUrl)
    console.log('[API] Request data:', config.data)
    return config
  },
  (error) => {
    console.error('[API] Request error:', error)
    return Promise.reject(error)
  }
)

// Add response interceptor to log API responses
api.interceptors.response.use(
  (response) => {
    console.log('[API] Response received from:', response.config.url)
    console.log('[API] Response data:', response.data)
    return response
  },
  (error) => {
    console.error('[API] Response error:', error.message)
    console.error('[API] Error details:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export interface MoodAnalysisRequest {
  text: string
  user_id?: string
}

export interface MoodAnalysisResponse {
  success: boolean
  mood_analysis: {
    sentiment: {
      label: string
      score: number
    }
    emotions: Record<string, number>
    mood_score: number
    text_length: number
  }
  crisis_check: {
    risk_level: 'LOW' | 'MEDIUM' | 'HIGH'
    indicators: string[]
    requires_immediate_attention: boolean
    resources: Array<{
      name: string
      phone: string
      text?: string
      available: string
      priority?: string
    }>
    ai_reasoning?: string
    ai_enhanced?: boolean
  }
  recommendations: Array<{
    type: string
    title: string
    description: string
    priority: string
    source?: string
    ai_enhanced?: boolean
  }>
}

export interface MoodHistoryEntry {
  timestamp: string
  mood_score: number
  sentiment: {
    label: string
    score: number
  }
  emotions: Record<string, number>
  text: string
}

export const moodAPI = {
  analyze: async (request: MoodAnalysisRequest): Promise<MoodAnalysisResponse> => {
    const response = await api.post<MoodAnalysisResponse>('/api/mood/analyze', request)
    return response.data
  },

  getHistory: async (user_id: string = 'default_user', days: number = 30) => {
    const response = await api.get<{
      success: boolean
      entries: MoodHistoryEntry[]
      total_entries: number
    }>(`/api/mood/history?user_id=${user_id}&days=${days}`)
    return response.data
  },

  predict: async (user_id: string = 'default_user') => {
    const response = await api.post<{
      success: boolean
      prediction: any
    }>('/api/mood/predict', { user_id, days: 30 })
    return response.data
  },
}

export const insightsAPI = {
  getPatterns: async (user_id: string = 'default_user') => {
    const response = await api.get(`/api/insights/patterns?user_id=${user_id}`)
    return response.data
  },

  getRecommendations: async (user_id: string = 'default_user') => {
    const response = await api.get(`/api/insights/recommendations?user_id=${user_id}`)
    return response.data
  },
}

export const crisisAPI = {
  check: async (text: string, user_id: string = 'default_user') => {
    const response = await api.post('/api/crisis/check', { text, user_id })
    return response.data
  },

  getResources: async () => {
    const response = await api.get('/api/crisis/resources')
    return response.data
  },
}

export const devAPI = {
  seedDemoData: async () => {
    const response = await api.post('/api/dev/seed')
    return response.data
  },
}


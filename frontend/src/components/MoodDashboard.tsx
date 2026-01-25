'use client'

import { useState, useEffect } from 'react'
import { ArrowRight, RefreshCw, CheckCircle2 } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, AreaChart, Area } from 'recharts'
import { moodAPI, insightsAPI, devAPI, MoodHistoryEntry } from '@/services/api'

export default function MoodDashboard() {
  const [history, setHistory] = useState<MoodHistoryEntry[]>([])
  const [patterns, setPatterns] = useState<any>(null)
  const [recommendations, setRecommendations] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [seeding, setSeeding] = useState(false)
  const [showToast, setShowToast] = useState(false)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      const [historyData, patternsData, recsData] = await Promise.all([
        moodAPI.getHistory('demo_user', 30),
        insightsAPI.getPatterns('demo_user'),
        insightsAPI.getRecommendations('demo_user'),
      ])
      
      setHistory(historyData.entries)
      setPatterns(patternsData.patterns)
      setRecommendations(recsData.recommendations)
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSeedDemoData = async () => {
    setSeeding(true)
    try {
      await devAPI.seedDemoData()
      setShowToast(true)
      // Reload dashboard data
      await loadDashboardData()
      // Hide toast after 3 seconds
      setTimeout(() => setShowToast(false), 3000)
    } catch (error) {
      console.error('Error seeding demo data:', error)
      alert('Failed to load demo data. Please try again.')
    } finally {
      setSeeding(false)
    }
  }

  const chartData = history.map(entry => ({
    date: new Date(entry.timestamp).toLocaleDateString(),
    mood: entry.mood_score,
    timestamp: entry.timestamp,
  }))

  const emotionData = history.reduce((acc: Record<string, number>, entry) => {
    Object.entries(entry.emotions || {}).forEach(([emotion, score]) => {
      if (!acc[emotion]) acc[emotion] = 0
      acc[emotion] += score
    })
    return acc
  }, {})

  const topEmotions = Object.entries(emotionData)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 5)
    .map(([emotion, total]) => ({
      emotion,
      average: total / history.length,
    }))

  if (loading) {
    return (
      <div className="bg-white/10 backdrop-blur-sm rounded-xl shadow-lg border border-white/20 p-6 md:p-8 text-center">
        <div className="flex flex-col items-center gap-4">
          <svg className="animate-spin h-8 w-8 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p className="text-white font-medium">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  if (history.length === 0) {
    return (
      <div className="bg-white/10 backdrop-blur-sm rounded-xl shadow-lg border border-white/20 p-4 md:p-6 text-center">
        <p className="text-white font-medium mb-4">No mood data yet. Start analyzing your mood to see insights!</p>
        <div className="space-y-3">
          <p className="text-sm text-white/80 font-medium">Go to the "Analyze Mood" tab to get started, or</p>
          <button
            onClick={handleSeedDemoData}
            disabled={seeding}
            className="px-8 py-4 bg-gradient-to-r from-primary-400 to-primary-500 text-white rounded-2xl font-semibold hover:from-primary-500 hover:to-primary-600 disabled:from-slate-400 disabled:to-slate-400 disabled:cursor-not-allowed transition-all duration-300 transform hover:-translate-y-1 hover:shadow-xl hover:shadow-primary-500/30 active:scale-95 shadow-lg shadow-primary-500/25 disabled:shadow-none flex items-center justify-center gap-2 mx-auto group"
          >
            {seeding ? (
              <>
                <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Loading Demo Data...</span>
              </>
            ) : (
              <>
                Load Demo Data
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </>
            )}
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Toast Notification */}
      {showToast && (
        <div className="fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-slide-in">
          <CheckCircle2 className="w-5 h-5 inline mr-2" />
          Demo Data Loaded Successfully!
        </div>
      )}

      {/* Demo Data Button (Top Right) */}
      <div className="flex justify-end">
        <button
          onClick={handleSeedDemoData}
          disabled={seeding}
          className="px-5 py-2.5 bg-white/10 hover:bg-white/20 text-white rounded-xl font-medium text-sm disabled:bg-white/5 disabled:cursor-not-allowed transition-all duration-200 transform active:scale-95 border border-white/20 hover:shadow-md hover:-translate-y-0.5 flex items-center gap-2 group"
        >
          {seeding ? 'Loading...' : (
            <>
              <RefreshCw className="w-4 h-4" /> Refresh Demo Data
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </>
          )}
        </button>
      </div>
      {/* Summary Cards - Color-Coded */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 md:gap-6">
        <div className={`rounded-2xl shadow-2xl p-8 transition-all duration-300 hover:shadow-3xl hover:-translate-y-1 text-white ${
          (patterns?.average_mood || 0) >= 7 
            ? 'bg-gradient-to-br from-green-500 to-emerald-600'
            : (patterns?.average_mood || 0) >= 4
            ? 'bg-gradient-to-br from-primary-400 to-primary-500'
            : 'bg-gradient-to-br from-orange-500 to-amber-600'
        }`}>
          <h3 className="text-xs font-semibold opacity-90 mb-3 tracking-wider uppercase">Average Mood</h3>
          <p className="text-6xl md:text-7xl font-extralight leading-none drop-shadow-lg">
            {patterns?.average_mood?.toFixed(1) || 'N/A'}
          </p>
        </div>
        <div className="bg-gradient-to-br from-cyan-500 to-teal-600 rounded-2xl shadow-2xl p-8 transition-all duration-300 hover:shadow-3xl hover:-translate-y-1 text-white">
          <h3 className="text-xs font-semibold opacity-90 mb-3 tracking-wider uppercase">Total Entries</h3>
          <p className="text-6xl md:text-7xl font-extralight leading-none drop-shadow-lg">{history.length}</p>
        </div>
        <div className={`rounded-2xl shadow-2xl p-8 transition-all duration-300 hover:shadow-3xl hover:-translate-y-1 text-white ${
          patterns?.trend === 'IMPROVING' 
            ? 'bg-gradient-to-br from-green-500 to-emerald-600'
            : patterns?.trend === 'DECLINING'
            ? 'bg-gradient-to-br from-red-500 to-red-600'
            : 'bg-gradient-to-br from-primary-400 to-primary-500'
        }`}>
          <h3 className="text-xs font-semibold opacity-90 mb-3 tracking-wider uppercase">Trend</h3>
          <p className="text-5xl md:text-6xl font-extralight leading-none drop-shadow-lg">
            {patterns?.trend || 'STABLE'}
          </p>
        </div>
      </div>

      {/* Mood Trend Chart */}
      <div className="bg-white/10 backdrop-blur-sm rounded-2xl shadow-2xl border border-white/20 p-8">
        <h2 className="text-2xl md:text-3xl font-bold text-white mb-8 tracking-tight">Mood Trend Over Time</h2>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="colorMood" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#2B7A78" stopOpacity={0.4}/>
                <stop offset="50%" stopColor="#3AAFA9" stopOpacity={0.2}/>
                <stop offset="95%" stopColor="#3AAFA9" stopOpacity={0}/>
              </linearGradient>
              <filter id="glow">
                <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                <feMerge>
                  <feMergeNode in="coloredBlur"/>
                  <feMergeNode in="SourceGraphic"/>
                </feMerge>
              </filter>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis dataKey="date" stroke="rgba(255,255,255,0.7)" />
            <YAxis domain={[0, 10]} stroke="rgba(255,255,255,0.7)" />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
              }}
            />
            <Area 
              type="monotone" 
              dataKey="mood" 
              stroke="#2B7A78" 
              strokeWidth={3}
              fillOpacity={1}
              fill="url(#colorMood)"
              dot={{ r: 5, fill: '#2B7A78', strokeWidth: 2, stroke: '#fff' }}
              activeDot={{ r: 7, fill: '#3AAFA9' }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Emotion Analysis */}
      <div className="bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl border border-slate-200/50 p-8">
        <h2 className="text-2xl md:text-3xl font-bold text-slate-800 mb-8 tracking-tight">Common Emotions</h2>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={topEmotions}>
            <defs>
              <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#2B7A78" stopOpacity={0.9}/>
                <stop offset="100%" stopColor="#3AAFA9" stopOpacity={0.7}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="emotion" stroke="#6b7280" />
            <YAxis stroke="#6b7280" />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
              }}
            />
            <Bar dataKey="average" fill="url(#barGradient)" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* AI-Generated Pattern Insights */}
      {patterns && patterns.ai_insight && (
        <div className="bg-gradient-to-br from-purple-500 to-indigo-600 rounded-2xl shadow-2xl p-6 md:p-8 text-white transition-all duration-300 hover:shadow-3xl hover:-translate-y-1">
          <div className="flex items-start gap-3 mb-4">
            <div className="bg-white/20 rounded-lg p-2">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <div className="flex-1">
              <h3 className="text-lg md:text-xl font-bold mb-2 flex items-center gap-2">
                AI-Generated Insight
                <span className="text-xs bg-white/20 px-2 py-1 rounded-full">Powered by TELUS AI Factory</span>
              </h3>
              <p className="text-base md:text-lg leading-relaxed opacity-95">{patterns.ai_insight}</p>
            </div>
          </div>
        </div>
      )}

      {/* Patterns */}
      {patterns && patterns.patterns && patterns.patterns.length > 0 && (
        <div className="bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl border border-slate-200/50 p-8">
          <h2 className="text-2xl md:text-3xl font-bold text-slate-800 mb-6 tracking-tight">Identified Patterns</h2>
          <div className="space-y-2">
            {patterns.patterns.map((pattern: any, idx: number) => (
              <div key={idx} className="p-3 bg-blue-50 rounded-lg">
                <p className="text-gray-700">{pattern.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations */}
      {recommendations && recommendations.length > 0 && (
        <div className="bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl border border-slate-200/50 p-8">
          <h2 className="text-2xl md:text-3xl font-bold text-slate-800 mb-6 tracking-tight">Personalized Recommendations</h2>
          <div className="space-y-3">
            {recommendations.map((rec: any, idx: number) => (
              <div
                key={idx}
                className="p-5 bg-gradient-to-r from-blue-50 to-primary-50 rounded-xl border-l-4 border-primary-500 shadow-sm transition-all duration-300 hover:shadow-md"
                style={{ animationDelay: `${idx * 100}ms` }}
              >
                <h3 className="font-semibold text-slate-800 mb-2">{rec.title}</h3>
                <p className="text-sm text-slate-700 leading-relaxed font-medium opacity-90">{rec.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}


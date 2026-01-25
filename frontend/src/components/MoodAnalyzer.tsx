'use client'

import { useState } from 'react'
import { Camera, FlaskConical, ArrowRight, AlertTriangle } from 'lucide-react'
import { moodAPI, MoodAnalysisResponse } from '@/services/api'
import TestPrompts from './TestPrompts'
import FaceScanner from './FaceScanner'

export default function MoodAnalyzer() {
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<MoodAnalysisResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [showTestPrompts, setShowTestPrompts] = useState(false)
  const [showFaceScanner, setShowFaceScanner] = useState(false)

  const handleAnalyze = async () => {
    if (!text.trim()) {
      setError('Please enter some text to analyze')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      console.log('[MoodAnalyzer] Calling API with text:', text)
      const response = await moodAPI.analyze({ text, user_id: 'default_user' })
      console.log('[MoodAnalyzer] API response received:', response)
      setResult(response)
    } catch (err: any) {
      console.error('[MoodAnalyzer] API error:', err)
      console.error('[MoodAnalyzer] Error details:', err.response?.data || err.message)
      setError(err.response?.data?.detail || `Failed to analyze mood: ${err.message}. Is the backend running?`)
    } finally {
      setLoading(false)
    }
  }

  const getMoodColor = (score: number) => {
    if (score >= 7) return 'text-green-600'
    if (score >= 4) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getMoodLabel = (score: number) => {
    if (score >= 8) return 'Excellent'
    if (score >= 6) return 'Good'
    if (score >= 4) return 'Moderate'
    if (score >= 2) return 'Low'
    return 'Very Low'
  }

  const handleFaceEmotionDetected = async (emotions: { [key: string]: number }, moodScore: number) => {
    // Convert emotions to text description for API
    const topEmotions = Object.entries(emotions)
      .filter(([_, value]) => value > 0.1)
      .sort(([_, a], [__, b]) => b - a)
      .slice(0, 3)
      .map(([emotion]) => emotion)
    
    const emotionText = `I'm feeling ${topEmotions.join(', ')} based on my facial expression.`
    
    setText(emotionText)
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await moodAPI.analyze({ text: emotionText, user_id: 'default_user' })
      // Override mood score with face detection result
      response.mood_analysis.mood_score = moodScore
      response.mood_analysis.emotions = emotions
      setResult(response)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze mood. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-transparent rounded-2xl p-6 md:p-8">
      {/* Supportive Headline - BetterHelp Style */}
      <div className="text-center mb-8">
        <h2 className="text-3xl md:text-4xl font-bold text-white drop-shadow-sm mb-3 leading-tight tracking-tight">
          You deserve to feel better
        </h2>
        <p className="text-lg md:text-xl text-green-50 font-medium">
          How are you feeling today?
        </p>
      </div>

      <div className="mb-8">
        <h3 className="text-xl md:text-2xl font-bold text-white drop-shadow-sm mb-4 tracking-tight">Mood Analysis</h3>
        <p className="text-sm text-green-50 font-medium mb-6">Share your thoughts and get instant insights</p>
        
        {/* Prominent Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <button
            onClick={() => setShowFaceScanner(true)}
            className="flex-1 px-6 py-4 bg-white/15 hover:bg-white/25 text-white hover:text-green-100 rounded-2xl font-semibold text-base md:text-lg transition-all duration-300 flex items-center justify-center gap-3 border-2 border-white/30 backdrop-blur-md shadow-xl hover:shadow-2xl hover:-translate-y-1 hover:scale-[1.02] group"
          >
            <Camera className="w-6 h-6 md:w-7 md:h-7" />
            <span>Face Scan</span>
            <ArrowRight className="w-5 h-5 md:w-6 md:h-6 group-hover:translate-x-1 transition-transform" />
          </button>
          <button
            onClick={() => setShowTestPrompts(!showTestPrompts)}
            className="flex-1 px-6 py-4 bg-white/15 hover:bg-white/25 text-white hover:text-green-100 rounded-2xl font-semibold text-base md:text-lg transition-all duration-300 flex items-center justify-center gap-3 border-2 border-white/30 backdrop-blur-md shadow-xl hover:shadow-2xl hover:-translate-y-1 hover:scale-[1.02] group"
          >
            <FlaskConical className="w-6 h-6 md:w-7 md:h-7" />
            <span>{showTestPrompts ? 'Hide' : 'Sample Messages'}</span>
            <ArrowRight className="w-5 h-5 md:w-6 md:h-6 group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
      </div>
      
      {/* Sample Messages Section - Only visible when toggled */}
      {showTestPrompts && (
        <div className="mb-6">
          <TestPrompts onSelectPrompt={(prompt) => {
            setText(prompt)
            setShowTestPrompts(false) // Hide after selection
          }} />
        </div>
      )}
      
      <div className="mb-8">
        <label className="block text-sm font-semibold text-green-50 mb-3 tracking-wide">
          How are you feeling today?
        </label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Share your thoughts, feelings, or what's on your mind..."
          className="w-full h-36 p-5 border border-white/20 rounded-2xl focus:ring-2 focus:ring-white/40 focus:border-white/30 focus:shadow-lg resize-none transition-all duration-300 leading-relaxed text-white placeholder:text-green-100/60 font-medium bg-white/10 backdrop-blur-md shadow-lg"
          disabled={loading}
        />
        <div className="flex flex-col sm:flex-row gap-3 mt-6">
          <button
            onClick={handleAnalyze}
            disabled={loading || !text.trim()}
            className="flex-1 bg-white text-green-800 py-4 px-8 rounded-2xl font-bold text-base hover:bg-green-50 hover:shadow-[0_0_20px_rgba(255,255,255,0.4)] disabled:bg-slate-400 disabled:text-slate-600 disabled:cursor-not-allowed transition-all duration-300 transform hover:-translate-y-1 active:scale-[0.98] shadow-lg disabled:shadow-none flex items-center justify-center gap-2 group"
          >
            {loading ? (
              <>
                <svg className="animate-spin h-5 w-5 text-green-800" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                Analyze My Mood
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </>
            )}
          </button>
          {!showTestPrompts && (
            <button
              onClick={() => setShowTestPrompts(true)}
              className="px-5 py-4 bg-white/10 hover:bg-white/20 text-white hover:text-green-200 rounded-2xl font-medium transition-all duration-200 transform active:scale-95 border border-white/20 backdrop-blur-md shadow-lg"
              title="Show sample messages"
            >
              <FlaskConical className="w-5 h-5" />
            </button>
          )}
        </div>
      </div>

      {error && (
        <div className="mb-4 p-4 bg-red-500/20 border border-red-400/50 rounded-lg text-white backdrop-blur-sm">
          {error}
        </div>
      )}

      {result && (
        <div className="space-y-6">
          {/* Mood Score - Color-Coded Based on Score */}
          <div className={`rounded-2xl p-8 md:p-10 shadow-2xl text-white transition-all duration-300 hover:shadow-3xl hover:-translate-y-1 ${
            result.mood_analysis.mood_score >= 7 
              ? 'bg-gradient-to-br from-green-500 to-emerald-600'
              : result.mood_analysis.mood_score >= 4
              ? 'bg-gradient-to-br from-primary-400 to-primary-500'
              : 'bg-gradient-to-br from-orange-500 to-amber-600'
          }`}>
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
              <div>
                <h3 className="text-sm font-semibold uppercase tracking-wider mb-2 opacity-90">Your Mood Score</h3>
                <p className="text-base opacity-90 leading-relaxed">
                  Mood Level: <span className="font-bold">{getMoodLabel(result.mood_analysis.mood_score)}</span>
                </p>
              </div>
              <div className="text-center md:text-right">
                <div className="flex items-baseline justify-center md:justify-end gap-2">
                  <span className="text-6xl md:text-8xl font-extralight leading-none drop-shadow-lg">
                    {result.mood_analysis.mood_score.toFixed(1)}
                  </span>
                  <span className="text-2xl md:text-3xl font-light opacity-80">/10</span>
                </div>
              </div>
            </div>
          </div>

          {/* Sentiment - Color-Coded Card */}
          <div className={`rounded-2xl p-6 shadow-xl transition-all duration-300 hover:shadow-2xl hover:-translate-y-1 ${
            result.mood_analysis.sentiment.label === 'POSITIVE' 
              ? 'bg-gradient-to-br from-green-500 to-green-600 text-white'
              : result.mood_analysis.sentiment.label === 'NEGATIVE'
              ? 'bg-gradient-to-br from-orange-500 to-amber-600 text-white'
              : 'bg-gradient-to-br from-primary-400 to-primary-500 text-white'
          }`}>
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-sm font-semibold uppercase tracking-wider mb-2 opacity-90">Sentiment</h3>
                <div className="flex items-center gap-3">
                  <span className="text-2xl md:text-3xl font-bold">
                    {result.mood_analysis.sentiment.label}
                  </span>
                  <span className="text-sm opacity-90">
                    {(result.mood_analysis.sentiment.score * 100).toFixed(0)}% confidence
                  </span>
                </div>
              </div>
              <ArrowRight className="w-6 h-6 opacity-80" />
            </div>
          </div>

          {/* Emotions - Color-Coded Card */}
          <div className="bg-gradient-to-br from-cyan-500 to-teal-600 rounded-2xl p-6 shadow-xl text-white transition-all duration-300 hover:shadow-2xl hover:-translate-y-1">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold uppercase tracking-wider opacity-90">Detected Emotions</h3>
              <ArrowRight className="w-5 h-5 opacity-80" />
            </div>
            <div className="flex flex-wrap gap-3">
              {Object.entries(result.mood_analysis.emotions)
                .sort(([, a], [, b]) => b - a)
                .slice(0, 5)
                .map(([emotion, score]) => (
                  <div
                    key={emotion}
                    className="px-4 py-2 bg-white/20 backdrop-blur-sm rounded-full text-sm font-semibold border border-white/30 shadow-sm"
                  >
                    <span className="capitalize">{emotion}</span>: <span className="font-bold">{(score * 100).toFixed(0)}%</span>
                  </div>
                ))}
            </div>
          </div>

               {/* Crisis Alert - Color-Coded Red Card */}
               {result.crisis_check.requires_immediate_attention && (
                 <div className="bg-gradient-to-br from-red-600 to-red-700 rounded-2xl p-6 shadow-2xl text-white transition-all duration-300 hover:shadow-3xl hover:-translate-y-1">
                   <div className="flex items-start justify-between mb-4">
                     <div>
                       <h3 className="text-xl font-bold mb-2 flex items-center gap-2">
                         <AlertTriangle className="w-5 h-5" />
                         Immediate Support Available
                       </h3>
                       <p className="text-sm opacity-90 mb-4">
                         We detected indicators that you may need immediate support. Please reach out:
                       </p>
                       {result.crisis_check.ai_reasoning && (
                         <div className="mb-4 p-3 bg-white/10 rounded-lg border border-white/20">
                           <p className="text-xs font-semibold mb-1 opacity-80">AI Analysis:</p>
                           <p className="text-sm opacity-90">{result.crisis_check.ai_reasoning}</p>
                           <p className="text-xs mt-2 opacity-70">Powered by TELUS AI Factory (deepseekv32)</p>
                         </div>
                       )}
                     </div>
                     <ArrowRight className="w-6 h-6 opacity-80" />
                   </div>
              <div className="space-y-3">
                {result.crisis_check.resources.slice(0, 2).map((resource, idx) => (
                  <div key={idx} className="bg-white/20 backdrop-blur-sm p-4 rounded-xl border border-white/30 transition-all duration-200 hover:bg-white/30">
                    <p className="font-bold text-base mb-1">{resource.name}</p>
                    <p className="text-sm opacity-90">Phone: <span className="font-semibold">{resource.phone}</span></p>
                    {resource.text && <p className="text-sm opacity-90">Text: <span className="font-semibold">{resource.text}</span></p>}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Recommendations - Color-Coded Cards */}
          <div className="space-y-4">
            <h3 className="text-sm font-semibold text-white drop-shadow-sm uppercase tracking-wider mb-4">Personalized Recommendations</h3>
            {result.recommendations
              .sort((a: any, b: any) => {
                // Sort by priority: CRITICAL > HIGH > MEDIUM > LOW
                const priorityOrder: { [key: string]: number } = {
                  'CRITICAL': 0,
                  'HIGH': 1,
                  'MEDIUM': 2,
                  'LOW': 3
                }
                return (priorityOrder[a.priority] || 99) - (priorityOrder[b.priority] || 99)
              })
              .map((rec: any, idx) => (
              <div
                key={idx}
                className={`p-6 rounded-2xl shadow-xl transition-all duration-300 hover:shadow-2xl hover:-translate-y-1 cursor-pointer group backdrop-blur-md border ${
                  rec.priority === 'CRITICAL' || rec.priority === 'HIGH'
                    ? 'bg-white/20 text-white border-white/30'
                    : rec.priority === 'MEDIUM'
                    ? 'bg-white/15 text-white border-white/25'
                    : 'bg-white/10 text-white border-white/20'
                }`}
                style={{ animationDelay: `${idx * 100}ms` }}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <h4 className="font-bold text-base md:text-lg mb-2">{rec.title}</h4>
                    <p className="text-sm opacity-90 leading-relaxed">{rec.description}</p>
                  </div>
                  <div className="flex flex-col items-end gap-2">
                    <ArrowRight className="w-5 h-5 opacity-80 group-hover:translate-x-1 transition-transform" />
                    <span className={`px-3 py-1 rounded-lg text-xs font-bold tracking-wide whitespace-nowrap ${
                      rec.priority === 'HIGH' 
                        ? 'bg-white/20 text-white border border-white/30'
                        : rec.priority === 'MEDIUM'
                        ? 'bg-white/20 text-white border border-white/30'
                        : 'bg-white/20 text-white border border-white/30'
                    }`}>
                      {rec.priority}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Face Scanner Modal */}
      {showFaceScanner && (
        <FaceScanner
          onEmotionDetected={handleFaceEmotionDetected}
          onClose={() => setShowFaceScanner(false)}
        />
      )}
    </div>
  )
}


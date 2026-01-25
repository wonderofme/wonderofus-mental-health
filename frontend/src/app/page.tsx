'use client'

import { useState } from 'react'
import MoodAnalyzer from '@/components/MoodAnalyzer'
import MoodDashboard from '@/components/MoodDashboard'
import CrisisResources from '@/components/CrisisResources'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'analyze' | 'dashboard' | 'resources'>('analyze')

  return (
    <main className="min-h-screen betterhelp-bg relative overflow-hidden">
      {/* Subtle radial gradient overlay for depth */}
      <div className="fixed inset-0 pointer-events-none z-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-white/10 via-transparent to-transparent"></div>
      
      {/* Subtle bottom wave - BetterHelp Style */}
      <div className="fixed bottom-0 left-0 right-0 pointer-events-none overflow-hidden z-0">
        <svg className="absolute bottom-0 w-full h-32" viewBox="0 0 1200 120" preserveAspectRatio="none">
          <path d="M0,120 Q200,90 400,100 T800,95 T1200,100 L1200,120 Z" fill="rgba(59, 175, 169, 0.15)" />
        </svg>
      </div>
      
      <div className="container mx-auto px-4 py-6 md:py-8 relative z-10">
        {/* Header */}
        <header className="text-center mb-8 md:mb-10">
          <div className="inline-block mb-4">
            <h1 className="text-4xl md:text-6xl font-extrabold text-white drop-shadow-sm mb-3 tracking-tight">
              WonderOfUs
            </h1>
          </div>
          <p className="text-xl md:text-2xl font-semibold text-green-50 mb-3 leading-tight tracking-tight">
            AI Mental Health Companion
          </p>
          <p className="text-sm md:text-base text-green-50/80 leading-relaxed max-w-2xl mx-auto">
            Built for TELUS Hackathon 2025 • AI at the Edge of Innovation
          </p>
        </header>

        {/* Navigation Tabs - BetterHelp Style */}
        <div className="flex justify-center mb-8 md:mb-10">
          <div className="inline-flex bg-white/10 backdrop-blur-md rounded-2xl shadow-lg border border-white/20 p-1.5 gap-1">
            <button
              onClick={() => setActiveTab('analyze')}
              className={`px-6 md:px-8 py-2.5 rounded-xl font-medium text-sm md:text-base transition-all duration-300 ${
                activeTab === 'analyze'
                  ? 'bg-white text-green-800 shadow-lg font-semibold'
                  : 'text-white hover:text-green-200 hover:bg-white/10'
              }`}
            >
              Analyze Mood
            </button>
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`px-6 md:px-8 py-2.5 rounded-xl font-medium text-sm md:text-base transition-all duration-300 ${
                activeTab === 'dashboard'
                  ? 'bg-white text-green-800 shadow-lg font-semibold'
                  : 'text-white hover:text-green-200 hover:bg-white/10'
              }`}
            >
              Dashboard
            </button>
            <button
              onClick={() => setActiveTab('resources')}
              className={`px-6 md:px-8 py-2.5 rounded-xl font-medium text-sm md:text-base transition-all duration-300 ${
                activeTab === 'resources'
                  ? 'bg-white text-green-800 shadow-lg font-semibold'
                  : 'text-white hover:text-green-200 hover:bg-white/10'
              }`}
            >
              Resources
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="max-w-6xl mx-auto">
          {activeTab === 'analyze' && <MoodAnalyzer />}
          {activeTab === 'dashboard' && <MoodDashboard />}
          {activeTab === 'resources' && <CrisisResources />}
        </div>
      </div>
    </main>
  )
}


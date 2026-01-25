'use client'

import { useState, useEffect } from 'react'
import { ArrowRight, AlertTriangle } from 'lucide-react'
import { crisisAPI } from '@/services/api'

export default function CrisisResources() {
  const [resources, setResources] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadResources()
  }, [])

  const loadResources = async () => {
    try {
      const response = await crisisAPI.getResources()
      setResources(response.resources || [])
    } catch (error) {
      console.error('Error loading resources:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="bg-white/10 backdrop-blur-sm rounded-xl shadow-lg border border-white/20 p-6 md:p-8 text-center">
        <div className="flex flex-col items-center gap-4">
          <svg className="animate-spin h-8 w-8 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p className="text-white font-medium">Loading resources...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white/10 backdrop-blur-sm rounded-xl shadow-lg border border-white/20 p-4 md:p-6">
      <h2 className="text-xl md:text-2xl font-bold text-white mb-2 tracking-tight">Crisis Support Resources</h2>
      <p className="text-white/90 mb-6 font-medium leading-relaxed">
        If you're experiencing a mental health crisis, these resources are available 24/7:
      </p>

      <div className="space-y-4">
        {resources.map((resource, idx) => (
          <div
            key={idx}
            className={`p-4 md:p-5 rounded-xl border-2 transition-all duration-200 hover:shadow-md ${
              resource.priority === 'IMMEDIATE'
                ? 'bg-red-50 border-red-300'
                : 'bg-primary-50 border-primary-200'
            }`}
          >
            <div className="flex items-start justify-between mb-3">
              <h3 className="text-xl font-bold">{resource.name}</h3>
              <div className="flex items-center gap-2">
                {resource.priority && (
                  <span className="px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full text-xs font-bold border border-white/30">
                    {resource.priority}
                  </span>
                )}
                <ArrowRight className="w-5 h-5 opacity-80 group-hover:translate-x-1 transition-transform" />
              </div>
            </div>
            
            {resource.description && (
              <p className="text-sm opacity-90 mb-4 leading-relaxed">{resource.description}</p>
            )}

            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="font-semibold opacity-90">Phone:</span>
                <a
                  href={`tel:${resource.phone}`}
                  className="font-bold underline hover:opacity-80 transition-opacity"
                >
                  {resource.phone}
                </a>
              </div>
              
              {resource.text && (
                <div className="flex items-center gap-2">
                  <span className="font-semibold opacity-90">Text:</span>
                  <span className="font-semibold">{resource.text}</span>
                </div>
              )}

              {resource.website && (
                <div className="flex items-center gap-2">
                  <span className="font-semibold opacity-90">Website:</span>
                  <a
                    href={resource.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="underline hover:opacity-80 transition-opacity"
                  >
                    {resource.website}
                  </a>
                </div>
              )}

              <div className="flex items-center gap-2">
                <span className="font-semibold opacity-90">Available:</span>
                <span className="font-semibold">{resource.available}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-xl">
        <p className="text-yellow-800 font-semibold">
          <div className="flex items-start gap-2">
            <AlertTriangle className="w-5 h-5 flex-shrink-0 mt-0.5" />
            <span>If you or someone else is in immediate danger, call 911 or go to your nearest emergency room.</span>
          </div>
        </p>
      </div>
    </div>
  )
}


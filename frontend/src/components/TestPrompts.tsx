'use client'

import { useState } from 'react'
import { FlaskConical, ArrowRight, ChevronDown, ChevronRight } from 'lucide-react'

interface TestPrompt {
  category: string
  description: string
  prompts: string[]
}

const testPrompts: TestPrompt[] = [
  {
    category: 'Positive/High Mood',
    description: 'Test positive sentiment and high mood scores',
    prompts: [
      "I'm feeling really great today! I just got a promotion at work and I'm so excited about the future.",
      "Had an amazing day with friends. We went hiking and the weather was perfect. Feeling grateful and happy!",
      "Feeling optimistic and energized. I've been making good progress on my goals and everything seems to be falling into place."
    ]
  },
  {
    category: 'Negative/Low Mood',
    description: 'Test negative sentiment and low mood scores',
    prompts: [
      "I'm feeling really anxious about my upcoming exam. I can't stop worrying about whether I'll pass or not.",
      "I've been feeling really down lately. Nothing seems to be going right and I'm struggling to find motivation.",
      "I'm so stressed out. Work is overwhelming, I have too many deadlines, and I feel like I'm drowning."
    ]
  },
  {
    category: 'Mixed/Complex Emotions',
    description: 'Test complex emotional states',
    prompts: [
      "I'm feeling conflicted. Part of me is excited about the new opportunity, but I'm also scared of the change.",
      "Today was a rollercoaster. Had some great moments but also some really frustrating ones. Overall feeling okay though."
    ]
  },
  {
    category: 'Crisis Detection',
    description: 'Test automatic crisis detection and resources',
    prompts: [
      "I feel hopeless and don't see a way out of this situation. Nothing matters anymore.",
      "I've been thinking about ending it all. Life just doesn't seem worth living right now."
    ]
  },
  {
    category: 'Neutral/Everyday',
    description: 'Test neutral sentiment detection',
    prompts: [
      "Just another regular day. Nothing special happened, feeling pretty neutral about everything.",
      "Feeling okay today. Not great, not terrible, just kind of existing."
    ]
  },
  {
    category: 'Specific Emotions',
    description: 'Test specific emotion detection (anger, sadness, fear)',
    prompts: [
      "I'm so angry right now! Someone cut me off in traffic and I'm still fuming about it.",
      "Feeling really sad after watching a movie. It brought up some old memories that made me emotional.",
      "I'm terrified about the presentation tomorrow. My heart is racing just thinking about it."
    ]
  }
]

interface TestPromptsProps {
  onSelectPrompt: (prompt: string) => void
}

export default function TestPrompts({ onSelectPrompt }: TestPromptsProps) {
  const [expandedCategory, setExpandedCategory] = useState<string | null>(null)

  const handlePromptClick = (prompt: string) => {
    onSelectPrompt(prompt)
    // Scroll to top of analyzer
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <div className="bg-white/10 backdrop-blur-md rounded-xl shadow-lg border border-white/20 p-4 md:p-6 mt-6">
      <h2 className="text-xl md:text-2xl font-bold text-white drop-shadow-sm mb-2 flex items-center gap-2">
        <FlaskConical className="w-5 h-5" />
        Sample Messages
      </h2>
      <p className="text-green-50 mb-4 font-medium">
        Click any message below to try it out. Messages are organized by category.
      </p>

      <div className="space-y-3">
        {testPrompts.map((category, idx) => (
          <div key={idx} className="border border-white/30 rounded-lg overflow-hidden">
            <button
              onClick={() => setExpandedCategory(
                expandedCategory === category.category ? null : category.category
              )}
              className="w-full px-4 py-3 bg-white/10 hover:bg-white/20 backdrop-blur-md transition-all duration-200 transform active:scale-[0.98] flex items-center justify-between rounded-lg border border-white/20 shadow-lg"
            >
              <div className="text-left flex-1">
                <h3 className="font-bold text-white text-base mb-1">{category.category}</h3>
                <p className="text-sm text-white/90 font-medium">{category.description}</p>
              </div>
              {expandedCategory === category.category ? (
                <ChevronDown className="w-5 h-5 text-white ml-4" />
              ) : (
                <ChevronRight className="w-5 h-5 text-white ml-4" />
              )}
            </button>

            {expandedCategory === category.category && (
              <div className="p-4 bg-white/5 space-y-2">
                {category.prompts.map((prompt, promptIdx) => (
                  <button
                    key={promptIdx}
                    onClick={() => handlePromptClick(prompt)}
                    className="w-full text-left p-3 bg-white/10 hover:bg-white/20 border border-white/30 rounded-xl transition-all duration-200 transform active:scale-[0.98] group shadow-sm hover:shadow-md"
                  >
                    <div className="flex items-start justify-between">
                      <p className="text-white text-sm font-semibold flex-1 group-hover:text-primary-300">
                        {prompt}
                      </p>
                      <ArrowRight className="ml-2 w-4 h-4 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="mt-4 p-3 bg-yellow-500/20 border border-yellow-400/50 rounded-xl backdrop-blur-sm">
        <p className="text-sm text-white">
          <strong>Tip:</strong> After analyzing a few prompts, check the Dashboard tab to see mood trends and patterns!
        </p>
      </div>
    </div>
  )
}


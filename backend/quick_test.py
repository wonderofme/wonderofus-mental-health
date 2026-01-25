# Quick test of crisis detection
import sys
sys.path.insert(0, '.')
from app.services.ai_service import ai_service

text = "I've been thinking about ending it all. Life just doesn't seem worth living right now."
print('Testing text:', text)
print()

# Test keyword matching
text_lower = text.lower()
keywords = ['ending it all', 'not worth living', 'been thinking about ending']
print('Keyword matching:')
for kw in keywords:
    print(f'  "{kw}" in text: {kw in text_lower}')
print()

# Test full crisis detection
mood = ai_service.analyze_mood(text)
print('Mood analysis:', mood)
print()

crisis = ai_service.detect_crisis_indicators(text, mood)
print('Crisis detection result:')
print(f'  risk_level: {crisis.get("risk_level")}')
print(f'  requires_immediate_attention: {crisis.get("requires_immediate_attention")}')
print(f'  indicators: {crisis.get("indicators")}')


"""Test crisis detection"""
from app.services.ai_service import ai_service

test_cases = [
    "I've been thinking about ending it all",
    "I have been thinking about ending it all",
    "I've been thinking about ending it all. Life just doesn't seem worth living right now.",
]

for text in test_cases:
    print(f"\nTesting: '{text}'")
    mood = ai_service.analyze_mood(text)
    crisis = ai_service.detect_crisis_indicators(text, mood)
    print(f"  Risk Level: {crisis.get('risk_level')}")
    print(f"  Requires Attention: {crisis.get('requires_immediate_attention')}")
    print(f"  Indicators: {crisis.get('indicators')}")


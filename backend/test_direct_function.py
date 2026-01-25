"""Test the crisis detection function directly"""
import sys
sys.path.insert(0, '.')
from app.services.ai_service import ai_service

# Exact text from the user
text = "I've been thinking about ending it all. Life just doesn't seem worth living right now."

print("="*60)
print("DIRECT FUNCTION TEST")
print("="*60)
print(f"Text: {text}")
print()

# Analyze mood first
mood = ai_service.analyze_mood(text)
print("Mood Analysis:")
print(f"  Mood Score: {mood.get('mood_score')}")
print(f"  Sentiment: {mood.get('sentiment', {}).get('label')}")
print()

# Now test crisis detection
print("Crisis Detection:")
crisis = ai_service.detect_crisis_indicators(text, mood)
print(f"  Risk Level: {crisis.get('risk_level')}")
print(f"  Requires Attention: {crisis.get('requires_immediate_attention')}")
print(f"  Indicators: {crisis.get('indicators')}")
print()

# Check if it should be HIGH
if crisis.get('risk_level') != 'HIGH':
    print("❌ ERROR: Risk level should be HIGH but got", crisis.get('risk_level'))
    print("\nChecking keywords manually...")
    text_lower = text.lower()
    keywords = [
        "thinking about ending it all",
        "been thinking about ending",
        "ending it all",
        "not worth living"
    ]
    for kw in keywords:
        if kw in text_lower:
            print(f"  ✓ '{kw}' MATCHES")
        else:
            print(f"  ✗ '{kw}' does NOT match")
else:
    print("✓ SUCCESS: Risk level is HIGH as expected")


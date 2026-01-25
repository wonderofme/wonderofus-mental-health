"""Test the actual API endpoint"""
import requests
import json

# Test the crisis detection endpoint
url = "http://127.0.0.1:8000/api/mood/analyze"
data = {
    "text": "I've been thinking about ending it all. Life just doesn't seem worth living right now.",
    "user_id": "test_user"
}

print("Testing API endpoint...")
print(f"URL: {url}")
print(f"Data: {data}")
print("\n" + "="*60)

response = requests.post(url, json=data)
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    print("\nResponse:")
    print(json.dumps(result, indent=2))
    
    print("\n" + "="*60)
    print("\nCRISIS CHECK:")
    crisis = result.get("crisis_check", {})
    print(f"  Risk Level: {crisis.get('risk_level')}")
    print(f"  Requires Attention: {crisis.get('requires_immediate_attention')}")
    print(f"  Indicators: {crisis.get('indicators')}")
    
    print("\nRECOMMENDATIONS:")
    recommendations = result.get("recommendations", [])
    for i, rec in enumerate(recommendations, 1):
        print(f"\n  {i}. {rec.get('title')}")
        print(f"     Priority: {rec.get('priority')}")
        print(f"     Type: {rec.get('type')}")
        print(f"     Source: {rec.get('source', 'N/A')}")
        print(f"     Description: {rec.get('description')[:80]}...")
    
    # Check if crisis recommendations are present
    crisis_recs = [r for r in recommendations if r.get('type') in ['CRISIS', 'PROFESSIONAL', 'SUPPORT']]
    wellness_recs = [r for r in recommendations if r.get('type') in ['WELLNESS', 'ACTIVITY']]
    print(f"\n  Crisis Recommendations: {len(crisis_recs)}")
    print(f"  Wellness Recommendations: {len(wellness_recs)}")
    if len(wellness_recs) > 0 and crisis_check.get('risk_level') == 'HIGH':
        print("  *** ERROR: Wellness recommendations shown during HIGH risk crisis! ***")
else:
    print(f"Error: {response.text}")


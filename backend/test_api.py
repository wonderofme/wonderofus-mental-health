"""Simple test script for the mood analysis API"""
import requests
import json

# Test the mood analysis endpoint
url = "http://localhost:8000/api/mood/analyze"
data = {
    "text": "test message for this",
    "user_id": "test_user"
}

try:
    print("Testing mood analysis API...")
    print(f"Text: '{data['text']}'")
    print("\nSending request...")
    
    response = requests.post(url, json=data, timeout=30)
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n[SUCCESS] Response received:")
        print(json.dumps(result, indent=2))
    else:
        print(f"\n[ERROR] Status Code: {response.status_code}")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print("[ERROR] Could not connect to server. Is it running on http://localhost:8000?")
except requests.exceptions.Timeout:
    print("[ERROR] Request timed out. The AI models might still be loading.")
except Exception as e:
    print(f"[ERROR] {e}")


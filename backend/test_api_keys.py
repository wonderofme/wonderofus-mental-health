"""
Test script to check if TELUS AI Factory API keys are still active
"""
from openai import OpenAI
import sys

def test_gemma_api():
    """Test Gemma-3-27b API"""
    print("Testing Gemma-3-27b API...")
    try:
        client = OpenAI(
            base_url="https://gemma-3-27b-3ca9s.paas.ai.telus.com/v1",
            api_key="dc8704d41888afb2b889a8ebac81d12f"
        )
        response = client.completions.create(
            model="google/gemma-3-27b-it",
            prompt="Say hello in one word.",
            max_tokens=10
        )
        print("[OK] Gemma API: WORKING")
        print(f"   Response: {response.choices[0].text.strip()}")
        return True
    except Exception as e:
        print("[FAIL] Gemma API: FAILED")
        print(f"   Error: {str(e)[:200]}")
        return False

def test_deepseek_api():
    """Test DeepSeekV32 API"""
    print("\nTesting DeepSeekV32 API...")
    try:
        client = OpenAI(
            base_url="https://deepseekv32-3ca9s.paas.ai.telus.com/v1",
            api_key="a12a7d3705b12aeb46eb4cc8d77f5446"
        )
        response = client.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            prompt="Say hello in one word.",
            max_tokens=10
        )
        print("[OK] DeepSeek API: WORKING")
        print(f"   Response: {response.choices[0].text.strip()}")
        return True
    except Exception as e:
        print("[FAIL] DeepSeek API: FAILED")
        print(f"   Error: {str(e)[:200]}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("TELUS AI Factory API Key Status Check")
    print("=" * 60)
    
    gemma_works = test_gemma_api()
    deepseek_works = test_deepseek_api()
    
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Gemma-3-27b: {'[ACTIVE]' if gemma_works else '[DEACTIVATED/ERROR]'}")
    print(f"  DeepSeekV32: {'[ACTIVE]' if deepseek_works else '[DEACTIVATED/ERROR]'}")
    print("=" * 60)
    
    if not gemma_works and not deepseek_works:
        print("\n[WARNING] Both API keys appear to be deactivated or endpoints changed.")
        print("   The app will still work but TELUS AI features will use fallback responses.")
    elif not gemma_works or not deepseek_works:
        print("\n[WARNING] One API key appears to be deactivated.")
        print("   Some TELUS AI features may not work.")
    else:
        print("\n[SUCCESS] All API keys are active!")


"""Debug keyword matching"""
text = "I've been thinking about ending it all. Life just doesn't seem worth living right now."
text_lower = text.lower()
print(f"Text (lowercase): {text_lower}")
print()

high_risk_keywords = [
    "suicide", "kill myself", "end it all", "ending it all", "not worth living",
    "want to die", "hurt myself", "self harm", "end my life",
    "take my life", "kill myself", "no reason to live", "thinking about ending",
    "thinking of ending", "considering ending", "planning to end",
    "thinking about ending it all", "thinking of ending it all",
    "been thinking about ending", "been thinking of ending"
]

print("Checking keywords (sorted by length, longest first):")
sorted_keywords = sorted(high_risk_keywords, key=len, reverse=True)
for keyword in sorted_keywords:
    match = keyword in text_lower
    print(f"  '{keyword}' -> {match}")
    if match:
        print(f"    ✓ MATCHED!")
        break


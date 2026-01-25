"""Detailed keyword matching test"""
text = "I've been thinking about ending it all. Life just doesn't seem worth living right now."

# Exact keywords from the code
high_risk_keywords = [
    "suicide", "kill myself", "end it all", "ending it all", "not worth living",
    "want to die", "hurt myself", "self harm", "end my life",
    "take my life", "kill myself", "no reason to live", "thinking about ending",
    "thinking of ending", "considering ending", "planning to end",
    "thinking about ending it all", "thinking of ending it all",
    "been thinking about ending", "been thinking of ending"
]

text_lower = text.lower()
print(f"Original text: {text}")
print(f"Lowercase text: {text_lower}")
print(f"Text length: {len(text_lower)}")
print()

print("Checking all keywords (sorted by length, longest first):")
sorted_keywords = sorted(high_risk_keywords, key=len, reverse=True)
matches = []
for keyword in sorted_keywords:
    match = keyword in text_lower
    if match:
        matches.append(keyword)
        print(f"  [MATCH] '{keyword}' -> Found at position {text_lower.find(keyword)}")
    else:
        print(f"  [NO MATCH] '{keyword}'")

print()
if matches:
    print(f"FIRST MATCH (should be used): {matches[0]}")
    print(f"Risk level should be: HIGH")
else:
    print("NO MATCHES FOUND - This is the problem!")


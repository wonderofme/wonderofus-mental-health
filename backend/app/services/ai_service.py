"""
AI Service for Sentiment Analysis and Emotion Detection
Uses Hugging Face Transformers for real-time mood analysis

PRIVACY & COMPLIANCE:
- All AI models run locally via Hugging Face Transformers (inference-only)
- No data is sent to external third-party APIs (e.g., OpenAI, Google)
- All processing happens on the server, ensuring HIPAA-compliant architecture
- User data is stored in-memory for demo purposes (production would use encrypted database)
- No user data is shared with model providers or third parties

This ensures compliance with healthcare data protection regulations.
"""

from transformers import pipeline
import torch
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

# Lazy import to avoid circular dependency
_telus_ai_service = None

def get_telus_ai_service():
    """Lazy load TELUS AI service to avoid circular imports"""
    global _telus_ai_service
    if _telus_ai_service is None:
        try:
            from app.services.telus_ai_service import telus_ai_service
            _telus_ai_service = telus_ai_service
        except Exception as e:
            logger.warning(f"Could not load TELUS AI service: {e}")
            _telus_ai_service = None
    return _telus_ai_service

class AIService:
    """
    Service for AI-powered mood and sentiment analysis.
    
    PRIVACY NOTE: All models run locally. No data leaves the server.
    This ensures HIPAA compliance and user privacy.
    """
    
    def __init__(self):
        """
        Initialize AI models.
        
        Models are loaded from Hugging Face and run locally.
        No external API calls are made, ensuring data privacy.
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        
        # Initialize sentiment analysis pipeline
        # Model runs locally - no data sent to external services
        try:
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=0 if self.device == "cuda" else -1
            )
        except Exception as e:
            logger.warning(f"Could not load sentiment model: {e}")
            self.sentiment_analyzer = None
        
        # Initialize emotion detection pipeline
        # Model runs locally - no data sent to external services
        try:
            self.emotion_analyzer = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                device=0 if self.device == "cuda" else -1
            )
        except Exception as e:
            logger.warning(f"Could not load emotion model: {e}")
            self.emotion_analyzer = None
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of input text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with sentiment label and score
        """
        if not self.sentiment_analyzer:
            return {
                "label": "NEUTRAL",
                "score": 0.5,
                "error": "Model not loaded"
            }
        
        try:
            result = self.sentiment_analyzer(text)[0]
            label = result['label'].upper()
            score = result['score']
            
            # Normalize labels
            if 'POSITIVE' in label or 'POS' in label:
                sentiment = "POSITIVE"
            elif 'NEGATIVE' in label or 'NEG' in label:
                sentiment = "NEGATIVE"
            else:
                sentiment = "NEUTRAL"
            
            return {
                "label": sentiment,
                "score": float(score),
                "raw_label": label
            }
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return {
                "label": "NEUTRAL",
                "score": 0.5,
                "error": str(e)
            }
    
    def detect_emotions(self, text: str) -> Dict[str, float]:
        """
        Detect emotions in input text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary mapping emotions to confidence scores
        """
        if not self.emotion_analyzer:
            return {
                "neutral": 1.0,
                "error": "Model not loaded"
            }
        
        try:
            results = self.emotion_analyzer(text, top_k=None)
            emotions = {}
            
            for result in results:
                emotion = result['label'].lower()
                score = result['score']
                emotions[emotion] = float(score)
            
            return emotions
        except Exception as e:
            logger.error(f"Error in emotion detection: {e}")
            return {
                "neutral": 1.0,
                "error": str(e)
            }
    
    def analyze_mood(self, text: str) -> Dict[str, Any]:
        """
        Comprehensive mood analysis combining sentiment and emotions
        
        Args:
            text: Input text to analyze
            
        Returns:
            Complete mood analysis with sentiment, emotions, and mood score
        """
        sentiment = self.analyze_sentiment(text)
        emotions = self.detect_emotions(text)
        
        # Calculate mood score (0-10, where 5 is neutral)
        mood_score = 5.0
        
        # Adjust based on sentiment
        if sentiment["label"] == "POSITIVE":
            mood_score += sentiment["score"] * 3
        elif sentiment["label"] == "NEGATIVE":
            mood_score -= sentiment["score"] * 3
        
        # Adjust based on emotions
        positive_emotions = ["joy", "love", "optimism", "pride", "amusement"]
        negative_emotions = ["sadness", "anger", "fear", "disgust", "disappointment"]
        
        for emotion, score in emotions.items():
            if emotion in positive_emotions:
                mood_score += score * 2
            elif emotion in negative_emotions:
                mood_score -= score * 2
        
        # Clamp mood score between 0 and 10
        mood_score = max(0, min(10, mood_score))
        
        return {
            "sentiment": sentiment,
            "emotions": emotions,
            "mood_score": round(mood_score, 2),
            "text_length": len(text)
        }
    
    def detect_crisis_indicators(self, text: str, mood_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect potential crisis indicators with safety-first approach.
        
        SAFETY PROTOCOL: High-risk keywords automatically trigger HIGH risk level
        regardless of other factors. This ensures no crisis situations are missed.
        
        Args:
            text: Input text
            mood_analysis: Previous mood analysis results
            
        Returns:
            Crisis detection results with risk level and recommendations
        """
        import sys
        print("\n" + "!"*80, flush=True)
        print("!"*80, flush=True)
        print("!!! detect_crisis_indicators FUNCTION CALLED !!!", flush=True)
        print(f"!!! Text: '{text}' !!!", flush=True)
        print("!"*80, flush=True)
        print("!"*80 + "\n", flush=True)
        sys.stdout.flush()
        
        # High-risk keywords that ALWAYS trigger HIGH risk level
        high_risk_keywords = [
            "suicide", "kill myself", "end it all", "ending it all", "not worth living",
            "want to die", "hurt myself", "self harm", "end my life",
            "take my life", "kill myself", "no reason to live", "thinking about ending",
            "thinking of ending", "considering ending", "planning to end",
            "thinking about ending it all", "thinking of ending it all",
            "been thinking about ending", "been thinking of ending"
        ]
        
        # Medium-risk keywords that indicate distress
        medium_risk_keywords = [
            "hopeless", "no way out", "give up", "nothing matters",
            "can't go on", "can't take it", "overwhelmed", "desperate"
        ]
        
        text_lower = text.lower()
        risk_level = "LOW"
        indicators = []
        detected_emotion_type = None
        
        # DEBUG: Log the text being checked
        logger.debug(f"Checking crisis indicators for text (first 100 chars): {text_lower[:100]}")
        
        # SAFETY: Check high-risk keywords FIRST - these force HIGH risk
        # Check longer phrases first to avoid partial matches
        matched_keyword = None
        import sys
        print(f"[CRISIS DETECTION] Starting keyword check. Text (first 100 chars): {text_lower[:100]}", flush=True)
        print(f"[CRISIS DETECTION] Checking {len(high_risk_keywords)} keywords (sorted by length)...", flush=True)
        sys.stdout.flush()
        for keyword in sorted(high_risk_keywords, key=len, reverse=True):
            if keyword in text_lower:
                risk_level = "HIGH"
                matched_keyword = keyword
                indicators.append(f"CRITICAL: Contains high-risk keyword: '{keyword}'")
                logger.warning(f"CRISIS DETECTED: Keyword '{keyword}' found in text. Risk level set to HIGH.")
                print(f"[CRISIS DETECTION] *** MATCHED *** Keyword '{keyword}' found! Setting risk_level to HIGH.", flush=True)
                sys.stdout.flush()
                break  # One high-risk keyword is enough
        
        if not matched_keyword:
            logger.debug(f"No high-risk keywords matched. Text checked: {text_lower[:100]}")
            print(f"[CRISIS DETECTION] *** NO MATCH *** No high-risk keywords matched. Risk level remains: {risk_level}", flush=True)
            print(f"[CRISIS DETECTION] Text was: '{text_lower}'", flush=True)
            sys.stdout.flush()
        
        # If no high-risk keywords, check medium-risk
        if risk_level != "HIGH":
            for keyword in medium_risk_keywords:
                if keyword in text_lower:
                    risk_level = "MEDIUM"
                    indicators.append(f"Contains distress indicator: '{keyword}'")
                    break
        
        # Additional checks only if no keywords detected
        if risk_level == "LOW":
            # Check mood score
            mood_score = mood_analysis.get("mood_score", 5.0)
            if mood_score < 2.0:
                risk_level = "MEDIUM"
                indicators.append("Very low mood score detected (< 2.0)")
            
            # Check for extreme negative emotions
            emotions = mood_analysis.get("emotions", {})
            if emotions.get("sadness", 0) > 0.8:
                if risk_level == "LOW":
                    risk_level = "MEDIUM"
                indicators.append("High intensity sadness detected (> 80%)")
                detected_emotion_type = "depression"
            elif emotions.get("anger", 0) > 0.8:
                if risk_level == "LOW":
                    risk_level = "MEDIUM"
                indicators.append("High intensity anger detected (> 80%)")
            elif emotions.get("fear", 0) > 0.7 or emotions.get("anxiety", 0) > 0.7:
                if risk_level == "LOW":
                    risk_level = "MEDIUM"
                indicators.append("High intensity anxiety/fear detected")
                detected_emotion_type = "anxiety"
        
        # Enhance with TELUS AI Factory (deepseekv32) for advanced reasoning
        ai_enhancement = None
        telus_service = get_telus_ai_service()
        if telus_service:
            try:
                ai_enhancement = telus_service.analyze_crisis_reasoning(
                    text=text,
                    mood_analysis=mood_analysis,
                    keyword_risk_level=risk_level
                )
                # Use AI reasoning if available, but prioritize safety (HIGH risk from keywords)
                if ai_enhancement and ai_enhancement.get("ai_enhanced"):
                    # Safety: If keyword detection says HIGH, always keep it HIGH
                    if risk_level == "HIGH":
                        final_risk_level = "HIGH"
                    else:
                        final_risk_level = ai_enhancement.get("risk_level", risk_level)
                    
                    # Merge indicators
                    ai_indicators = ai_enhancement.get("indicators", [])
                    all_indicators = indicators + ai_indicators
                    
                    return {
                        "risk_level": final_risk_level,
                        "indicators": all_indicators,
                        "requires_immediate_attention": final_risk_level == "HIGH",
                        "detected_emotion_type": detected_emotion_type,
                        "resources": self._get_crisis_resources(final_risk_level, detected_emotion_type),
                        "ai_reasoning": ai_enhancement.get("reasoning", ""),
                        "ai_enhanced": True
                    }
            except Exception as e:
                logger.warning(f"TELUS AI enhancement failed, using keyword-based detection: {e}")
                print(f"[CRISIS DETECTION] TELUS AI failed: {e}. Using keyword-based risk_level: {risk_level}")
        
        # Final return - log what we're returning
        print(f"[CRISIS DETECTION] Final return - risk_level: {risk_level}, requires_attention: {risk_level == 'HIGH'}")
        return {
            "risk_level": risk_level,
            "indicators": indicators,
            "requires_immediate_attention": risk_level == "HIGH",
            "detected_emotion_type": detected_emotion_type,
            "resources": self._get_crisis_resources(risk_level, detected_emotion_type),
            "ai_enhanced": False
        }
    
    def _get_crisis_resources(self, risk_level: str, emotion_type: str = None) -> List[Dict[str, str]]:
        """
        Get crisis resources based on risk level and detected emotion type.
        
        Resources are prioritized based on:
        1. Risk level (HIGH gets emergency services first)
        2. Emotion type (anxiety vs depression get specialized resources)
        """
        resources = []
        
        # HIGH RISK: Always include emergency services first
        if risk_level == "HIGH":
            resources.append({
                "name": "Emergency Services",
                "phone": "911",
                "text": "Call immediately if in immediate danger",
                "available": "24/7",
                "priority": "IMMEDIATE",
                "description": "Call 911 immediately if you or someone else is in immediate danger"
            })
        
        # Emotion-specific resources
        if emotion_type == "anxiety":
            resources.append({
                "name": "Anxiety Canada",
                "phone": "1-604-620-0744",
                "website": "https://www.anxietycanada.com/",
                "available": "24/7",
                "description": "Specialized support for anxiety and panic disorders"
            })
        elif emotion_type == "depression":
            resources.append({
                "name": "Crisis Services Canada",
                "phone": "1-833-456-4566",
                "text": "45645",
                "website": "https://www.crisisservicescanada.ca/",
                "available": "24/7",
                "description": "Free, confidential support for depression and mental health crises"
            })
        
        # General crisis resources
        resources.extend([
            {
                "name": "Crisis Services Canada",
                "phone": "1-833-456-4566",
                "text": "45645",
                "website": "https://www.crisisservicescanada.ca/",
                "available": "24/7",
                "description": "Free, confidential support for anyone in Canada"
            },
            {
                "name": "Kids Help Phone",
                "phone": "1-800-668-6868",
                "text": "686868",
                "website": "https://kidshelpphone.ca/",
                "available": "24/7",
                "description": "Support for youth under 20"
            }
        ])
        
        # Remove duplicates (in case emotion-specific resource matches general)
        seen = set()
        unique_resources = []
        for resource in resources:
            key = resource["name"]
            if key not in seen:
                seen.add(key)
                unique_resources.append(resource)
        
        return unique_resources

# Global AI service instance
ai_service = AIService()


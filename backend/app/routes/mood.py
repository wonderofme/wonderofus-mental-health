"""
Mood Analysis API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
from app.services.ai_service import ai_service
from app.services.mood_service import mood_service

logger = logging.getLogger(__name__)
router = APIRouter()


class MoodAnalysisRequest(BaseModel):
    text: str
    user_id: Optional[str] = "default_user"


class MoodHistoryRequest(BaseModel):
    user_id: Optional[str] = "default_user"
    days: Optional[int] = 30


@router.post("/analyze")
async def analyze_mood(request: MoodAnalysisRequest):
    """
    Analyze mood from text input using AI models.
    
    This endpoint performs:
    1. Sentiment analysis (positive/negative/neutral)
    2. Multi-emotion detection (joy, sadness, anxiety, anger, fear, etc.)
    3. Mood score calculation (0-10 scale)
    4. Crisis indicator detection
    5. Personalized recommendations (with TELUS AI Factory enhancement)
    
    Returns:
        MoodAnalysisResponse with sentiment, emotions, mood score,
        crisis check results, and personalized recommendations.
    """
    try:
        # Step 1: Perform AI-powered mood analysis
        logger.info(f"Analyzing mood for user: {request.user_id}")
        mood_analysis = ai_service.analyze_mood(request.text)
        mood_analysis["text"] = request.text
        
        # Step 2: Save to user's mood history
        mood_service.save_mood_entry(request.user_id, mood_analysis)
        
        # Step 3: Check for crisis indicators (safety-first approach)
        crisis_check = ai_service.detect_crisis_indicators(request.text, mood_analysis)
        
        # Step 4: Determine if crisis response is needed
        is_crisis = crisis_check.get("requires_immediate_attention") or crisis_check.get("risk_level") in ["HIGH", "CRITICAL"]
        
        # Log crisis detection for monitoring
        if is_crisis:
            logger.warning(f"CRISIS DETECTED for user {request.user_id}. Risk level: {crisis_check.get('risk_level')}. Showing crisis recommendations only.")
        else:
            logger.info(f"No crisis detected. Risk level: {crisis_check.get('risk_level')}. Showing normal recommendations.")
        
        if is_crisis:
            # CRISIS SITUATION: ONLY show crisis-appropriate recommendations
            # DO NOT show wellness activities like breathing exercises or light exercise
            recommendations = [
                {
                    "type": "CRISIS",
                    "title": "Immediate Support Available",
                    "description": "Your safety is our priority. Please reach out to crisis services immediately. You are not alone, and there are people who want to help you.",
                    "priority": "CRITICAL",
                    "source": "crisis_detection"
                },
                {
                    "type": "PROFESSIONAL",
                    "title": "Connect with a Mental Health Professional",
                    "description": "Consider speaking with a therapist, counselor, or mental health professional. They can provide the support and guidance you need during this difficult time.",
                    "priority": "HIGH",
                    "source": "crisis_detection"
                },
                {
                    "type": "SUPPORT",
                    "title": "Reach Out to Someone You Trust",
                    "description": "Talk to a friend, family member, or someone you trust. You don't have to go through this alone.",
                    "priority": "HIGH",
                    "source": "crisis_detection"
                }
            ]
        else:
            # Normal situation: Get regular recommendations
            recommendations = _get_recommendations(mood_analysis)
            
            # Try to enhance with TELUS AI if available (only for non-crisis situations)
            try:
                from app.services.telus_ai_service import telus_ai_service
                
                # mood_service is already imported at the top of the file
                patterns = mood_service.analyze_patterns(request.user_id)
                mood_history = mood_service.get_mood_history(request.user_id, days=14)
                
                # Generate AI recommendation (only for non-crisis situations)
                ai_rec = telus_ai_service.generate_personalized_recommendation(
                    current_mood=mood_analysis,
                    mood_history=mood_history,
                    patterns=patterns,
                    is_crisis=False  # Non-crisis only
                )
                
                # Add AI recommendation at the top
                recommendations.insert(0, ai_rec)
            except Exception as e:
                # If AI fails, continue with rule-based recommendations
                logger.warning(f"Could not generate AI recommendation: {e}")
        
        return {
            "success": True,
            "mood_analysis": mood_analysis,
            "crisis_check": crisis_check,
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing mood: {str(e)}")


@router.get("/history")
async def get_mood_history(user_id: str = "default_user", days: int = 30):
    """
    Get mood history for a user
    """
    try:
        history = mood_service.get_mood_history(user_id, days)
        return {
            "success": True,
            "user_id": user_id,
            "days": days,
            "entries": history,
            "total_entries": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")


@router.post("/predict")
async def predict_mood_trend(request: MoodHistoryRequest):
    """
    Predict future mood trends based on historical data
    """
    try:
        prediction = mood_service.predict_mood_trend(request.user_id)
        return {
            "success": True,
            "user_id": request.user_id,
            "prediction": prediction
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting mood: {str(e)}")


def _get_recommendations(mood_analysis: dict) -> list:
    """Generate personalized recommendations based on mood analysis"""
    recommendations = []
    mood_score = mood_analysis.get("mood_score", 5.0)
    emotions = mood_analysis.get("emotions", {})
    
    if mood_score < 4.0:
        recommendations.append({
            "type": "WELLNESS",
            "title": "Practice Deep Breathing",
            "description": "Take 5 deep breaths to help calm your mind",
            "priority": "HIGH"
        })
        recommendations.append({
            "type": "ACTIVITY",
            "title": "Light Exercise",
            "description": "A short walk or gentle movement can improve mood",
            "priority": "MEDIUM"
        })
    
    if emotions.get("anxiety", 0) > 0.6:
        recommendations.append({
            "type": "TECHNIQUE",
            "title": "Grounding Exercise",
            "description": "Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste",
            "priority": "HIGH"
        })
    
    if emotions.get("sadness", 0) > 0.6:
        recommendations.append({
            "type": "SUPPORT",
            "title": "Reach Out",
            "description": "Consider talking to a friend, family member, or mental health professional",
            "priority": "MEDIUM"
        })
    
    if mood_score > 7.0:
        recommendations.append({
            "type": "MAINTENANCE",
            "title": "Maintain Positive Habits",
            "description": "Keep doing what's working for you!",
            "priority": "LOW"
        })
    
    # Default recommendations if none match
    if not recommendations:
        recommendations.append({
            "type": "GENERAL",
            "title": "Stay Mindful",
            "description": "Continue tracking your mood and patterns",
            "priority": "LOW"
        })
    
    return recommendations


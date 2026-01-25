"""
Insights API Routes
"""

from fastapi import APIRouter, HTTPException
from app.services.mood_service import mood_service
from app.services.telus_ai_service import telus_ai_service

router = APIRouter()


@router.get("/patterns")
async def get_mood_patterns(user_id: str = "default_user"):
    """
    Get identified mood patterns for a user
    Enhanced with TELUS AI Factory (gemma-3-27b) for natural language insights
    """
    try:
        patterns = mood_service.analyze_patterns(user_id)
        mood_history = mood_service.get_mood_history(user_id, days=30)
        
        # Generate AI-powered natural language insights
        ai_insight = None
        try:
            ai_insight = telus_ai_service.generate_pattern_insights(
                patterns=patterns,
                mood_history=mood_history
            )
        except Exception as e:
            # If AI fails, continue without insight
            pass
        
        return {
            "success": True,
            "user_id": user_id,
            "patterns": patterns,
            "ai_insight": ai_insight,
            "ai_enhanced": ai_insight is not None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing patterns: {str(e)}")


@router.get("/recommendations")
async def get_recommendations(user_id: str = "default_user"):
    """
    Get personalized recommendations based on mood patterns
    Enhanced with TELUS AI Factory (gemma-3-27b) for personalized AI-generated recommendations
    """
    try:
        patterns = mood_service.analyze_patterns(user_id)
        mood_history = mood_service.get_mood_history(user_id, days=14)
        
        recommendations = []
        
        # Get current mood (most recent entry)
        current_mood = mood_history[-1] if mood_history else {
            "mood_score": 5.0,
            "sentiment": {"label": "NEUTRAL"},
            "emotions": {}
        }
        
        # Generate AI-powered personalized recommendation using gemma-3-27b
        try:
            ai_recommendation = telus_ai_service.generate_personalized_recommendation(
                current_mood=current_mood,
                mood_history=mood_history,
                patterns=patterns
            )
            recommendations.append(ai_recommendation)
        except Exception as e:
            # Fallback to rule-based if AI fails
            if patterns.get("trend") == "DECLINING":
                recommendations.append({
                    "type": "URGENT",
                    "title": "Consider Professional Support",
                    "description": "Your mood trend shows a decline. Consider reaching out to a mental health professional.",
                    "priority": "HIGH",
                    "source": "fallback"
                })
        
        # Add rule-based recommendations as supplements
        if patterns.get("average_mood", 5.0) < 4.0:
            recommendations.append({
                "type": "WELLNESS",
                "title": "Focus on Self-Care",
                "description": "Your average mood is lower than ideal. Prioritize activities that bring you joy.",
                "priority": "MEDIUM",
                "source": "rule-based"
            })
        
        common_emotions = patterns.get("common_emotions", {})
        if "anxiety" in common_emotions and common_emotions["anxiety"] > 0.5:
            recommendations.append({
                "type": "TECHNIQUE",
                "title": "Anxiety Management",
                "description": "Consider practicing mindfulness, meditation, or breathing exercises regularly.",
                "priority": "MEDIUM",
                "source": "rule-based"
            })
        
        if not recommendations:
            recommendations.append({
                "type": "GENERAL",
                "title": "Continue Tracking",
                "description": "Keep monitoring your mood patterns to identify trends and triggers.",
                "priority": "LOW",
                "source": "fallback"
            })
        
        return {
            "success": True,
            "user_id": user_id,
            "recommendations": recommendations,
            "based_on": patterns,
            "ai_enhanced": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")


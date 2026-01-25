"""
Crisis Detection and Resources API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.ai_service import ai_service

router = APIRouter()


class CrisisCheckRequest(BaseModel):
    text: str
    user_id: Optional[str] = "default_user"


@router.post("/check")
async def check_crisis_indicators(request: CrisisCheckRequest):
    """
    Check text for crisis indicators and provide resources
    """
    try:
        # Analyze mood first
        mood_analysis = ai_service.analyze_mood(request.text)
        
        # Check for crisis indicators
        crisis_check = ai_service.detect_crisis_indicators(request.text, mood_analysis)
        
        return {
            "success": True,
            "crisis_detection": crisis_check,
            "mood_analysis": mood_analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking crisis indicators: {str(e)}")


@router.get("/resources")
async def get_crisis_resources():
    """
    Get crisis support resources
    """
    resources = [
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
        },
        {
            "name": "Hope for Wellness Helpline",
            "phone": "1-855-242-3310",
            "website": "https://www.hopeforwellness.ca/",
            "available": "24/7",
            "description": "Support for Indigenous peoples"
        },
        {
            "name": "Emergency Services",
            "phone": "911",
            "available": "24/7",
            "description": "Call immediately if you or someone else is in immediate danger",
            "priority": "IMMEDIATE"
        }
    ]
    
    return {
        "success": True,
        "resources": resources,
        "note": "If you're in immediate danger, call 911 or go to your nearest emergency room"
    }


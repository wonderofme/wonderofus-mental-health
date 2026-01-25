"""
Development/Demo endpoints for hackathon presentation
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import random
from app.services.mood_service import mood_service
from app.services.ai_service import ai_service

router = APIRouter()


@router.post("/seed")
async def seed_demo_data():
    """
    Seed demo data for hackathon presentation
    Creates 14 days of mood entries showing a recovery arc
    """
    try:
        user_id = "demo_user"
        
        # Clear existing demo data
        if user_id in mood_service.mood_history:
            mood_service.mood_history[user_id] = []
        
        # Generate 14 days of data (2 entries per day = 28 entries)
        base_date = datetime.utcnow() - timedelta(days=14)
        
        # Recovery arc: Start low, gradually improve
        entries = []
        
        for day in range(14):
            # Calculate day progress (0.0 to 1.0)
            day_progress = day / 13.0
            
            # Base mood improves from 2.5 to 7.5 over 14 days
            base_mood = 2.5 + (day_progress * 5.0)
            
            # Add some variation
            for entry_num in range(2):  # 2 entries per day
                # Morning entry (slightly lower) or afternoon entry (slightly higher)
                time_offset = -0.3 if entry_num == 0 else 0.3
                mood_score = base_mood + time_offset + random.uniform(-0.5, 0.5)
                mood_score = max(1.0, min(9.5, mood_score))  # Clamp to 1-9.5
                
                # Create timestamp (morning around 9 AM, afternoon around 3 PM)
                hour = 9 if entry_num == 0 else 15
                minute = random.randint(0, 59)
                timestamp = base_date + timedelta(days=day, hours=hour, minutes=minute)
                
                # Generate emotions based on mood score
                emotions = {}
                if mood_score < 4:
                    emotions = {
                        "sadness": random.uniform(0.6, 0.9),
                        "anxiety": random.uniform(0.5, 0.8),
                        "fear": random.uniform(0.3, 0.6),
                        "neutral": random.uniform(0.2, 0.4),
                    }
                elif mood_score < 6:
                    emotions = {
                        "neutral": random.uniform(0.5, 0.7),
                        "sadness": random.uniform(0.2, 0.4),
                        "anxiety": random.uniform(0.2, 0.4),
                        "joy": random.uniform(0.1, 0.3),
                    }
                else:
                    emotions = {
                        "joy": random.uniform(0.5, 0.8),
                        "neutral": random.uniform(0.3, 0.5),
                        "optimism": random.uniform(0.4, 0.7),
                        "sadness": random.uniform(0.0, 0.2),
                    }
                
                # Normalize emotions to sum to ~1.0
                total = sum(emotions.values())
                emotions = {k: v / total for k, v in emotions.items()}
                
                # Determine sentiment
                if mood_score >= 6:
                    sentiment_label = "POSITIVE"
                    sentiment_score = random.uniform(0.7, 0.95)
                elif mood_score <= 4:
                    sentiment_label = "NEGATIVE"
                    sentiment_score = random.uniform(0.7, 0.95)
                else:
                    sentiment_label = "NEUTRAL"
                    sentiment_score = random.uniform(0.6, 0.85)
                
                # Create sample text based on mood
                if mood_score < 4:
                    sample_texts = [
                        "Feeling really down today. Everything seems overwhelming.",
                        "Struggling with anxiety and can't seem to shake it off.",
                        "Having a tough day. Nothing seems to be going right.",
                    ]
                elif mood_score < 6:
                    sample_texts = [
                        "Feeling okay today. Not great, but managing.",
                        "It's been an average day. Some ups and downs.",
                        "Doing alright. Taking things one step at a time.",
                    ]
                else:
                    sample_texts = [
                        "Feeling really good today! Things are looking up.",
                        "Had a great day. Feeling positive and energized.",
                        "Feeling optimistic about the future. Making progress!",
                    ]
                
                entry = {
                    "timestamp": timestamp.isoformat(),
                    "mood_score": round(mood_score, 2),
                    "sentiment": {
                        "label": sentiment_label,
                        "score": round(sentiment_score, 3),
                        "raw_label": sentiment_label
                    },
                    "emotions": emotions,
                    "text": random.choice(sample_texts)
                }
                
                entries.append(entry)
        
        # Sort by timestamp
        entries.sort(key=lambda x: x["timestamp"])
        
        # Save to mood service
        mood_service.mood_history[user_id] = entries
        
        return {
            "success": True,
            "message": "Demo data seeded successfully",
            "entries_created": len(entries),
            "days_covered": 14,
            "user_id": user_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error seeding demo data: {str(e)}")


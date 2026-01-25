"""
Mood Service for tracking and analyzing mood patterns over time
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

class MoodService:
    """Service for mood tracking and pattern analysis"""
    
    def __init__(self):
        """Initialize mood service"""
        # In-memory storage for demo (replace with database in production)
        self.mood_history: Dict[str, List[Dict[str, Any]]] = {}
    
    def save_mood_entry(self, user_id: str, mood_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save a mood entry for a user
        
        Args:
            user_id: User identifier
            mood_data: Mood analysis data
            
        Returns:
            Saved mood entry with timestamp
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "mood_score": mood_data.get("mood_score", 5.0),
            "sentiment": mood_data.get("sentiment", {}),
            "emotions": mood_data.get("emotions", {}),
            "text": mood_data.get("text", "")
        }
        
        if user_id not in self.mood_history:
            self.mood_history[user_id] = []
        
        self.mood_history[user_id].append(entry)
        
        return entry
    
    def get_mood_history(self, user_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get mood history for a user
        
        Args:
            user_id: User identifier
            days: Number of days to retrieve
            
        Returns:
            List of mood entries
        """
        if user_id not in self.mood_history:
            return []
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        history = []
        for entry in self.mood_history[user_id]:
            entry_date = datetime.fromisoformat(entry["timestamp"])
            if entry_date >= cutoff_date:
                history.append(entry)
        
        return sorted(history, key=lambda x: x["timestamp"])
    
    def analyze_patterns(self, user_id: str) -> Dict[str, Any]:
        """
        Analyze mood patterns for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            Pattern analysis results
        """
        history = self.get_mood_history(user_id, days=30)
        
        if not history:
            return {
                "patterns": [],
                "trend": "INSUFFICIENT_DATA",
                "average_mood": 5.0
            }
        
        # Calculate average mood
        mood_scores = [entry["mood_score"] for entry in history]
        average_mood = sum(mood_scores) / len(mood_scores)
        
        # Determine trend
        if len(mood_scores) >= 7:
            recent_avg = sum(mood_scores[-7:]) / 7
            older_avg = sum(mood_scores[:-7]) / len(mood_scores[:-7]) if len(mood_scores) > 7 else recent_avg
            
            if recent_avg > older_avg + 0.5:
                trend = "IMPROVING"
            elif recent_avg < older_avg - 0.5:
                trend = "DECLINING"
            else:
                trend = "STABLE"
        else:
            trend = "INSUFFICIENT_DATA"
        
        # Identify common emotions
        all_emotions = {}
        for entry in history:
            emotions = entry.get("emotions", {})
            for emotion, score in emotions.items():
                if emotion not in all_emotions:
                    all_emotions[emotion] = []
                all_emotions[emotion].append(score)
        
        common_emotions = {
            emotion: sum(scores) / len(scores)
            for emotion, scores in all_emotions.items()
            if len(scores) >= 3
        }
        common_emotions = dict(sorted(common_emotions.items(), key=lambda x: x[1], reverse=True)[:5])
        
        patterns = []
        
        # Pattern: Time of day
        morning_moods = [e["mood_score"] for e in history if 6 <= datetime.fromisoformat(e["timestamp"]).hour < 12]
        afternoon_moods = [e["mood_score"] for e in history if 12 <= datetime.fromisoformat(e["timestamp"]).hour < 18]
        evening_moods = [e["mood_score"] for e in history if 18 <= datetime.fromisoformat(e["timestamp"]).hour < 24]
        
        if morning_moods and afternoon_moods and evening_moods:
            patterns.append({
                "type": "TIME_OF_DAY",
                "description": f"Morning: {sum(morning_moods)/len(morning_moods):.1f}, "
                              f"Afternoon: {sum(afternoon_moods)/len(afternoon_moods):.1f}, "
                              f"Evening: {sum(evening_moods)/len(evening_moods):.1f}"
            })
        
        return {
            "patterns": patterns,
            "trend": trend,
            "average_mood": round(average_mood, 2),
            "total_entries": len(history),
            "common_emotions": common_emotions,
            "mood_range": {
                "min": min(mood_scores),
                "max": max(mood_scores)
            }
        }
    
    def predict_mood_trend(self, user_id: str) -> Dict[str, Any]:
        """
        Predict future mood trends based on historical data
        
        Args:
            user_id: User identifier
            
        Returns:
            Mood prediction results
        """
        history = self.get_mood_history(user_id, days=30)
        
        if len(history) < 7:
            return {
                "prediction": "INSUFFICIENT_DATA",
                "confidence": 0.0,
                "next_week_forecast": []
            }
        
        mood_scores = [entry["mood_score"] for entry in history[-14:]]  # Last 2 weeks
        
        # Simple linear trend prediction
        if len(mood_scores) >= 7:
            recent_trend = (mood_scores[-1] - mood_scores[-7]) / 7
            
            # Predict next 7 days
            forecast = []
            current_mood = mood_scores[-1]
            
            for day in range(1, 8):
                predicted_mood = current_mood + (recent_trend * day)
                predicted_mood = max(0, min(10, predicted_mood))  # Clamp to 0-10
                forecast.append({
                    "day": day,
                    "predicted_mood": round(predicted_mood, 2),
                    "date": (datetime.utcnow() + timedelta(days=day)).isoformat()
                })
            
            return {
                "prediction": "IMPROVING" if recent_trend > 0.1 else "DECLINING" if recent_trend < -0.1 else "STABLE",
                "confidence": min(0.8, abs(recent_trend) * 10),
                "next_week_forecast": forecast,
                "trend_slope": round(recent_trend, 3)
            }
        
        return {
            "prediction": "INSUFFICIENT_DATA",
            "confidence": 0.0,
            "next_week_forecast": []
        }

# Global mood service instance
mood_service = MoodService()


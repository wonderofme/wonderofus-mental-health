"""
TELUS AI Factory Service
Integration with TELUS AI Factory models for enhanced AI capabilities

Models Available:
- gemma-3-27b: General AI (best default)
- deepseekv32: Reasoning and complex logic
- qwen-emb: Embeddings and vector search
- qwen3coder30b: Code generation and analysis
- gpt-oss-120b: Advanced AI (most powerful)
"""

from openai import OpenAI
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class TELUSAIService:
    """
    Service for TELUS AI Factory model integration.
    
    Uses OpenAI-compatible API to access TELUS AI Factory models.
    """
    
    def __init__(self):
        """Initialize TELUS AI Factory clients"""
        # Gemma-3-27b client (General AI - best default)
        self.gemma_client = OpenAI(
            base_url="https://gemma-3-27b-3ca9s.paas.ai.telus.com/v1",
            api_key="dc8704d41888afb2b889a8ebac81d12f"
        )
        
        # DeepSeekV32 client (Reasoning and complex logic)
        self.deepseek_client = OpenAI(
            base_url="https://deepseekv32-3ca9s.paas.ai.telus.com/v1",
            api_key="a12a7d3705b12aeb46eb4cc8d77f5446"
        )
    
    def generate_personalized_recommendation(
        self,
        current_mood: Dict[str, Any],
        mood_history: List[Dict[str, Any]],
        patterns: Dict[str, Any],
        is_crisis: bool = False
    ) -> Dict[str, Any]:
        """
        Generate personalized recommendation using gemma-3-27b
        
        Args:
            current_mood: Current mood analysis
            mood_history: Recent mood history
            patterns: Identified mood patterns
            
        Returns:
            Personalized recommendation with title, description, and priority
        """
        try:
            # Build context from mood data
            mood_score = current_mood.get("mood_score", 5.0)
            sentiment = current_mood.get("sentiment", {}).get("label", "NEUTRAL")
            top_emotions = sorted(
                current_mood.get("emotions", {}).items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            
            trend = patterns.get("trend", "STABLE")
            avg_mood = patterns.get("average_mood", 5.0)
            
            # Create prompt for personalized recommendation
            if is_crisis:
                prompt = f"""You are a compassionate mental health AI assistant. This is a CRISIS SITUATION requiring immediate support.

Current Mood:
- Mood Score: {mood_score}/10
- Sentiment: {sentiment}
- Top Emotions: {', '.join([f'{e[0]} ({e[1]:.0%})' for e in top_emotions])}

⚠️ CRITICAL: The user is in crisis. Your recommendation MUST prioritize:
1. Immediate professional support (crisis hotlines, mental health professionals)
2. Connecting with trusted people (friends, family)
3. Safety and immediate support resources

DO NOT suggest wellness activities like breathing exercises, light exercise, or self-care as primary recommendations. Those are not appropriate for crisis situations.

Provide a brief (2-3 sentences), empathetic recommendation focused on immediate support and professional help.

Recommendation:"""
            else:
                prompt = f"""You are a compassionate mental health AI assistant. Based on the following user data, provide a personalized, empathetic recommendation.

Current Mood:
- Mood Score: {mood_score}/10
- Sentiment: {sentiment}
- Top Emotions: {', '.join([f'{e[0]} ({e[1]:.0%})' for e in top_emotions])}

Mood Patterns:
- Trend: {trend}
- Average Mood: {avg_mood:.1f}/10

Provide a brief (2-3 sentences), supportive, and actionable recommendation. Be empathetic and specific. Focus on what the user can do right now to improve their wellbeing.

Recommendation:"""

            response = self.gemma_client.completions.create(
                model="google/gemma-3-27b-it",  # Model name from TELUS documentation
                prompt=prompt,
                max_tokens=200,
                temperature=0.7
            )
            
            recommendation_text = response.choices[0].text.strip()
            
            # Determine priority based on crisis status and mood score
            if is_crisis:
                priority = "CRITICAL"
                title = "Immediate Support Needed"
            elif mood_score < 3.0:
                priority = "HIGH"
                title = "Immediate Support Recommended"
            elif mood_score < 5.0:
                priority = "MEDIUM"
                title = "Wellness Focus"
            else:
                priority = "LOW"
                title = "Maintain Your Progress"
            
            return {
                "title": title,
                "description": recommendation_text,
                "priority": priority,
                "type": "AI_GENERATED",
                "source": "gemma-3-27b"
            }
            
        except Exception as e:
            logger.error(f"Error generating personalized recommendation: {e}")
            # Fallback to default recommendation
            return {
                "title": "Continue Tracking Your Mood",
                "description": "Keep monitoring your mood patterns to identify trends and triggers.",
                "priority": "LOW",
                "type": "FALLBACK",
                "error": str(e)
            }
    
    def analyze_crisis_reasoning(
        self,
        text: str,
        mood_analysis: Dict[str, Any],
        keyword_risk_level: str
    ) -> Dict[str, Any]:
        """
        Advanced crisis detection reasoning using deepseekv32
        
        Args:
            text: User input text
            mood_analysis: Mood analysis results
            keyword_risk_level: Risk level from keyword detection
            
        Returns:
            Enhanced crisis analysis with reasoning
        """
        try:
            mood_score = mood_analysis.get("mood_score", 5.0)
            sentiment = mood_analysis.get("sentiment", {}).get("label", "NEUTRAL")
            emotions = mood_analysis.get("emotions", {})
            
            # Create prompt for crisis reasoning
            prompt = f"""You are a mental health crisis assessment AI. Analyze the following situation and determine if immediate support is needed.

User Statement: "{text}"

Mood Analysis:
- Mood Score: {mood_score}/10
- Sentiment: {sentiment}
- Emotions: {emotions}

Initial Risk Assessment: {keyword_risk_level}

Analyze the context, nuance, and severity. Consider:
1. Is there immediate danger to self or others?
2. Are there subtle indicators of distress?
3. What is the emotional intensity?

Provide:
1. Risk Level (LOW, MEDIUM, HIGH, CRITICAL)
2. Brief reasoning (1-2 sentences explaining why)
3. Key indicators detected

Format your response as:
RISK_LEVEL: [level]
REASONING: [explanation]
INDICATORS: [list of key indicators]"""

            response = self.deepseek_client.completions.create(
                model="deepseek-ai/DeepSeek-V3",  # Model name for deepseekv32 endpoint
                prompt=prompt,
                max_tokens=300,
                temperature=0.3  # Lower temperature for more consistent reasoning
            )
            
            reasoning_text = response.choices[0].text.strip()
            
            # Parse response
            risk_level = keyword_risk_level  # Default to keyword-based
            reasoning = ""
            indicators = []
            
            lines = reasoning_text.split('\n')
            for line in lines:
                if line.startswith('RISK_LEVEL:'):
                    risk_level = line.split(':', 1)[1].strip()
                elif line.startswith('REASONING:'):
                    reasoning = line.split(':', 1)[1].strip()
                elif line.startswith('INDICATORS:'):
                    indicators_text = line.split(':', 1)[1].strip()
                    indicators = [i.strip() for i in indicators_text.split(',')]
            
            # Safety: If keyword detection says HIGH, always keep it HIGH
            if keyword_risk_level == "HIGH":
                risk_level = "HIGH"
            
            return {
                "risk_level": risk_level,
                "reasoning": reasoning if reasoning else "AI analysis indicates potential concern based on mood patterns and emotional state.",
                "indicators": indicators if indicators else ["Mood analysis suggests monitoring may be beneficial"],
                "ai_enhanced": True,
                "source": "deepseekv32"
            }
            
        except Exception as e:
            logger.error(f"Error in crisis reasoning: {e}")
            # Fallback to keyword-based detection
            return {
                "risk_level": keyword_risk_level,
                "reasoning": "Unable to perform advanced analysis. Using keyword-based detection.",
                "indicators": [],
                "ai_enhanced": False,
                "error": str(e)
            }
    
    def generate_pattern_insights(
        self,
        patterns: Dict[str, Any],
        mood_history: List[Dict[str, Any]]
    ) -> str:
        """
        Generate natural language insights from mood patterns using gemma-3-27b
        
        Args:
            patterns: Identified mood patterns
            mood_history: Full mood history
            
        Returns:
            Natural language insight text
        """
        try:
            trend = patterns.get("trend", "STABLE")
            avg_mood = patterns.get("average_mood", 5.0)
            common_emotions = patterns.get("common_emotions", {})
            time_patterns = patterns.get("time_patterns", {})
            
            # Build prompt for pattern insights
            prompt = f"""You are a mental health insights AI. Analyze the following mood patterns and provide a brief, empathetic insight (2-3 sentences).

Mood Patterns:
- Trend: {trend}
- Average Mood: {avg_mood:.1f}/10
- Common Emotions: {common_emotions}
- Time Patterns: {time_patterns}

Provide a supportive, human-readable insight that helps the user understand their mood patterns. Be specific and actionable.

Insight:"""

            response = self.gemma_client.completions.create(
                model="google/gemma-3-27b-it",  # Model name from TELUS documentation
                prompt=prompt,
                max_tokens=150,
                temperature=0.7
            )
            
            insight = response.choices[0].text.strip()
            return insight
            
        except Exception as e:
            logger.error(f"Error generating pattern insights: {e}")
            # Fallback to basic insight
            if trend == "IMPROVING":
                return "Your mood shows an improving trend. Keep up the positive momentum!"
            elif trend == "DECLINING":
                return "Your mood trend shows a decline. Consider reaching out for support."
            else:
                return "Continue tracking your mood to identify patterns and trends."


# Global TELUS AI service instance
telus_ai_service = TELUSAIService()


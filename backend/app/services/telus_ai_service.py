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
import os
from dotenv import load_dotenv

# Load environment variables early (before service initialization)
load_dotenv()

# Try to import Gemini, but make it optional
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

logger = logging.getLogger(__name__)


class TELUSAIService:
    """
    AI Service for mental health recommendations and analysis.
    
    Primary: Google Gemini API (when GEMINI_API_KEY is set)
    Fallback: TELUS AI Factory models (currently deactivated)
    """
    
    def __init__(self):
        """Initialize Gemini (primary) and TELUS AI Factory clients (fallback)"""
        # Gemma-3-27b client (General AI - best default)
        # Read from environment variables, fallback to hardcoded values for backward compatibility
        gemma_base_url = os.getenv(
            "TELUS_AI_GEMMA_BASE_URL",
            "https://gemma-3-27b-3ca9s.paas.ai.telus.com/v1"
        )
        gemma_api_key = os.getenv(
            "TELUS_AI_GEMMA_API_KEY",
            "dc8704d41888afb2b889a8ebac81d12f"
        )
        
        self.gemma_client = OpenAI(
            base_url=gemma_base_url,
            api_key=gemma_api_key
        )
        
        # DeepSeekV32 client (Reasoning and complex logic)
        deepseek_base_url = os.getenv(
            "TELUS_AI_DEEPSEEK_BASE_URL",
            "https://deepseekv32-3ca9s.paas.ai.telus.com/v1"
        )
        deepseek_api_key = os.getenv(
            "TELUS_AI_DEEPSEEK_API_KEY",
            "a12a7d3705b12aeb46eb4cc8d77f5446"
        )
        
        self.deepseek_client = OpenAI(
            base_url=deepseek_base_url,
            api_key=deepseek_api_key
        )
        
        # Initialize Gemini as fallback
        self.gemini_available = False
        self.gemini_model = None
        if GEMINI_AVAILABLE:
            gemini_api_key = os.getenv("GEMINI_API_KEY")
            if gemini_api_key:
                try:
                    genai.configure(api_key=gemini_api_key)
                    # Use gemini-2.5-flash (fast, free tier friendly) or gemini-2.5-pro (more capable)
                    self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
                    self.gemini_available = True
                    logger.info("Gemini API configured successfully as primary AI service")
                except Exception as e:
                    logger.warning(f"Failed to configure Gemini: {e}")
            else:
                logger.info("Gemini API key not found, will use fallback responses")
        else:
            logger.info("Gemini library not installed, will use fallback responses")
    
    def generate_personalized_recommendation(
        self,
        current_mood: Dict[str, Any],
        mood_history: List[Dict[str, Any]],
        patterns: Dict[str, Any],
        is_crisis: bool = False,
        user_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate personalized recommendation using gemma-3-27b
        
        Args:
            current_mood: Current mood analysis
            mood_history: Recent mood history
            patterns: Identified mood patterns
            is_crisis: Whether this is a crisis situation
            user_text: The actual user message (for context-aware recommendations)
            
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

User's Message: "{user_text if user_text else 'Not provided'}"

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
                # Include user's actual message for context-aware recommendations
                user_context = f'\nUser\'s Message: "{user_text}"' if user_text else ""
                
                prompt = f"""You are a compassionate mental health AI assistant. Based on the following user data, provide a personalized, empathetic recommendation that is SPECIFIC to their situation.

{user_context}

Current Mood:
- Mood Score: {mood_score}/10
- Sentiment: {sentiment}
- Top Emotions: {', '.join([f'{e[0]} ({e[1]:.0%})' for e in top_emotions])}

Mood Patterns:
- Trend: {trend}
- Average Mood: {avg_mood:.1f}/10

IMPORTANT: Your recommendation should be SPECIFIC to what the user mentioned. For example:
- If they mention exam anxiety → suggest study strategies, time management, test preparation tips
- If they mention work stress → suggest work-life balance, task prioritization, boundary setting
- If they mention relationship issues → suggest communication strategies, support resources
- If they mention general anxiety → suggest grounding techniques, breathing exercises

Provide a brief (2-3 sentences), supportive, and actionable recommendation that directly addresses their specific situation. Be empathetic and contextually relevant.

Recommendation:"""

            # Use Gemini as primary, TELUS AI as fallback (since TELUS AI is deactivated)
            recommendation_text = None
            
            # Try Gemini first (primary)
            if self.gemini_available and self.gemini_model:
                try:
                    response = self.gemini_model.generate_content(prompt)
                    recommendation_text = response.text.strip()
                    logger.info("Successfully used Gemini for recommendation")
                except Exception as gemini_error:
                    logger.warning(f"Gemini failed: {gemini_error}. Trying TELUS AI fallback...")
            
            # Fallback to TELUS AI if Gemini not available or failed
            if not recommendation_text:
                try:
                    response = self.gemma_client.completions.create(
                        model="google/gemma-3-27b-it",  # Model name from TELUS documentation
                        prompt=prompt,
                        max_tokens=200,
                        temperature=0.7
                    )
                    recommendation_text = response.choices[0].text.strip()
                    logger.info("Used TELUS AI Gemma as fallback")
                except Exception as e:
                    logger.warning(f"TELUS AI Gemma also failed: {e}")
            
            # If still no recommendation, use default
            if not recommendation_text:
                raise Exception("All AI services failed, using default recommendation")
            
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

            # Use Gemini as primary, TELUS AI as fallback (since TELUS AI is deactivated)
            reasoning_text = None
            
            # Try Gemini first (primary)
            if self.gemini_available and self.gemini_model:
                try:
                    response = self.gemini_model.generate_content(prompt)
                    reasoning_text = response.text.strip()
                    logger.info("Successfully used Gemini for crisis reasoning")
                except Exception as gemini_error:
                    logger.warning(f"Gemini failed: {gemini_error}. Trying TELUS AI fallback...")
            
            # Fallback to TELUS AI if Gemini not available or failed
            if not reasoning_text:
                try:
                    response = self.deepseek_client.completions.create(
                        model="deepseek-ai/DeepSeek-V3",  # Model name for deepseekv32 endpoint
                        prompt=prompt,
                        max_tokens=300,
                        temperature=0.3  # Lower temperature for more consistent reasoning
                    )
                    reasoning_text = response.choices[0].text.strip()
                    logger.info("Used TELUS AI DeepSeek as fallback")
                except Exception as e:
                    logger.warning(f"TELUS AI DeepSeek also failed: {e}")
            
            # If still no reasoning, use default
            if not reasoning_text:
                raise Exception("All AI services failed, using keyword-based detection")
            
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

            # Use Gemini as primary, TELUS AI as fallback (since TELUS AI is deactivated)
            insight = None
            
            # Try Gemini first (primary)
            if self.gemini_available and self.gemini_model:
                try:
                    response = self.gemini_model.generate_content(prompt)
                    insight = response.text.strip()
                    logger.info("Successfully used Gemini for pattern insights")
                except Exception as gemini_error:
                    logger.warning(f"Gemini failed: {gemini_error}. Trying TELUS AI fallback...")
            
            # Fallback to TELUS AI if Gemini not available or failed
            if not insight:
                try:
                    response = self.gemma_client.completions.create(
                        model="google/gemma-3-27b-it",  # Model name from TELUS documentation
                        prompt=prompt,
                        max_tokens=150,
                        temperature=0.7
                    )
                    insight = response.choices[0].text.strip()
                    logger.info("Used TELUS AI Gemma as fallback")
                except Exception as telus_error:
                    logger.warning(f"TELUS AI Gemma also failed: {telus_error}")
            
            # If still no insight, use default fallback
            if not insight:
                raise Exception("All AI services failed, using default insight")
            
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




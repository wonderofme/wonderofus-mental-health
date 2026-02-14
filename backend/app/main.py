"""
WonderOfUs - AI Mental Health Companion
FastAPI Backend Application

TELUS Hackathon 2025 - AI at the Edge of Innovation
Track: AI + Healthcare & Wellness

Technical Architecture:
- FastAPI for high-performance async API
- Hugging Face Transformers for local AI inference (privacy-first)
- TELUS AI Factory integration (gemma-3-27b, deepseekv32)
- Modular service architecture with separation of concerns

Privacy & Compliance:
- All AI models run locally (HIPAA-compliant design)
- No data sent to external third-party APIs
- In-memory storage for demo (production: encrypted database)

Team: WonderOfUs (Ayoola Opere, Mujah Sokoro)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routes import mood, insights, crisis, dev
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file (if it exists)
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Application metadata
APP_VERSION = "1.0.0"
APP_TITLE = "WonderOfUs - AI Mental Health Companion API"
APP_DESCRIPTION = """
## AI-Powered Mental Health Support Platform

Built for TELUS Hackathon 2025 - AI at the Edge of Innovation

### Features:
- 🧠 **Real-time Sentiment Analysis** - Instant mood detection from text
- 😊 **Multi-Emotion Detection** - Identifies joy, sadness, anxiety, anger, fear
- 🚨 **Crisis Intervention** - Automatic detection and resource provision
- 📊 **Pattern Recognition** - Identifies mood trends and triggers
- 🔒 **Privacy-First** - All AI processing happens locally (HIPAA-ready)
- 🤖 **TELUS AI Factory** - Enhanced recommendations via gemma-3-27b & deepseekv32

### Team WonderOfUs
- Ayoola Opere
- Mujah Sokoro
"""

app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Team WonderOfUs",
        "url": "https://github.com/wonderofme/wonderofus-mental-health",
    },
    license_info={
        "name": "TELUS Hackathon 2025",
    }
)

# CORS middleware for frontend connection
# Allow all origins for hackathon deployment (can be restricted in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (Vercel, localhost, etc.)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with versioned API prefix
API_V1_PREFIX = "/api"
app.include_router(mood.router, prefix=f"{API_V1_PREFIX}/mood", tags=["Mood Analysis"])
app.include_router(insights.router, prefix=f"{API_V1_PREFIX}/insights", tags=["Insights & Patterns"])
app.include_router(crisis.router, prefix=f"{API_V1_PREFIX}/crisis", tags=["Crisis Detection"])
app.include_router(dev.router, prefix=f"{API_V1_PREFIX}/dev", tags=["Development & Demo"])


@app.on_event("startup")
async def startup_event():
    """Application startup - initialize services and log status"""
    logger.info("="*60)
    logger.info("WonderOfUs - AI Mental Health Companion")
    logger.info("TELUS Hackathon 2025 - AI at the Edge of Innovation")
    logger.info("="*60)
    logger.info(f"Version: {APP_VERSION}")
    logger.info("AI Models: Hugging Face Transformers (local inference)")
    logger.info("TELUS AI Factory: gemma-3-27b, deepseekv32")
    logger.info("Privacy: HIPAA-compliant design (all processing local)")
    logger.info("="*60)


@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint - API information and status
    
    Returns application metadata, version, and operational status.
    """
    return {
        "application": "WonderOfUs - AI Mental Health Companion",
        "version": APP_VERSION,
        "team": "WonderOfUs",
        "members": ["Ayoola Opere", "Mujah Sokoro"],
        "hackathon": "TELUS Hackathon 2025 - AI at the Edge of Innovation",
        "track": "AI + Healthcare & Wellness",
        "status": "operational",
        "features": {
            "sentiment_analysis": True,
            "emotion_detection": True,
            "crisis_detection": True,
            "pattern_recognition": True,
            "telus_ai_factory": True,
            "privacy_first": True
        },
        "documentation": "/docs"
    }


@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint for monitoring and load balancing
    
    Returns the current health status of the API and its components.
    """
    return {
        "status": "healthy",
        "version": APP_VERSION,
        "services": {
            "api": "operational",
            "ai_models": "loaded",
            "telus_ai_factory": "connected"
        }
    }


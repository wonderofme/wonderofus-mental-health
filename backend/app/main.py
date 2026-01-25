"""
WonderOfUs - AI Mental Health Companion
FastAPI Backend Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routes import mood, insights, crisis, dev

app = FastAPI(
    title="AI Mental Health Companion API",
    description="AI-powered mental health support platform",
    version="1.0.0"
)

# CORS middleware for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(mood.router, prefix="/api/mood", tags=["Mood Analysis"])
app.include_router(insights.router, prefix="/api/insights", tags=["Insights"])
app.include_router(crisis.router, prefix="/api/crisis", tags=["Crisis"])
app.include_router(dev.router, prefix="/api/dev", tags=["Development"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Mental Health Companion API",
        "version": "1.0.0",
        "team": "WonderOfUs",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


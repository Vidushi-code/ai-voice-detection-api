"""
Main FastAPI Application Entry Point

This is the production-ready entry point for the AI Voice Detection API.
It initializes the FastAPI app, loads the ML model, and starts the server.

Usage:
    python main.py

Or with Uvicorn directly:
    uvicorn main:app --host 0.0.0.0 --port 8000
"""

import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import router, api_key_auth
from model.inference import InferenceEngine
import app.api as api_module


# Model path
MODEL_PATH = "model/voice_model.pkl"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager - loads model at startup.
    """
    print("\n" + "=" * 60)
    print("AI VOICE DETECTION API - STARTING")
    print("=" * 60)
    
    # Check if model exists
    if not os.path.exists(MODEL_PATH):
        print(f"\n❌ ERROR: Model file not found at {MODEL_PATH}")
        print("\nPlease train the model first:")
        print("  python train.py")
        print("\nOr download a pre-trained model to model/voice_model.pkl")
        sys.exit(1)
    
    # Load model
    print(f"\nLoading model from: {MODEL_PATH}")
    try:
        api_module.inference_engine = InferenceEngine(MODEL_PATH)
        print("✓ Model loaded successfully")
    except Exception as e:
        print(f"\n❌ ERROR: Failed to load model: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("SERVER READY")
    print("=" * 60)
    print("\nAPI Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")
    print(f"\nAPI Key: {api_key_auth.api_key}")
    print("\nExample Request:")
    print('  curl -X POST "http://localhost:8000/predict" \\')
    print(f'    -H "Authorization: Bearer {api_key_auth.api_key}" \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"audio_url": "https://example.com/audio.mp3"}\'')
    print("\n" + "=" * 60 + "\n")
    
    yield  # Server runs here
    
    # Cleanup on shutdown
    print("\nShutting down server...")


# Initialize FastAPI app
app = FastAPI(
    title="AI Voice Detection API",
    description="""
    **Production-ready API for detecting AI-generated voices vs human voices.**
    
    ## Features
    - Real-time voice classification
    - Multi-language support (Hindi/English)
    - Fraud risk assessment
    - Fast inference (< 2 seconds)
    - Explainable AI predictions
    
    ## Use Cases
    - Fraud prevention in voice-based authentication
    - Content verification for media platforms
    - Deepfake detection for cybersecurity
    - Quality assurance for voice recordings
    
    ## Technical Stack
    - **ML Model**: RandomForest Classifier
    - **Features**: MFCC + Spectral Analysis
    - **Framework**: FastAPI + Scikit-learn
    
    ## Authentication
    All endpoints (except health check) require Bearer token authentication.
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, tags=["Voice Detection"])


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Catch-all exception handler for production stability.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "detail": "An unexpected error occurred. Please try again.",
            "type": type(exc).__name__
        }
    )


# Entry point for direct execution
if __name__ == "__main__":
    import uvicorn
    
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    # Start server
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False,  # Set True for development
        log_level="info"
    )

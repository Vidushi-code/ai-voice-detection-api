"""
FastAPI Routes for Voice Detection API

Defines all API endpoints with request/response models and error handling.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
import time

from app.security import api_key_auth
from model.inference import InferenceEngine
from utils import AudioDownloadError, ValidationError, InputValidator


# Request/Response Models
class PredictionRequest(BaseModel):
    """
    API request model for voice detection.
    """
    audio_url: str = Field(
        ...,
        description="HTTP/HTTPS URL to audio file (MP3, WAV, FLAC, OGG)",
        example="https://example.com/audio/sample.mp3"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "audio_url": "https://example.com/audio/sample.mp3"
            }
        }


class PredictionResponse(BaseModel):
    """
    API response model for voice detection results.
    """
    label: str = Field(
        ...,
        description="Classification result: AI_GENERATED or HUMAN"
    )
    confidence: float = Field(
        ...,
        description="Prediction confidence score (0.0 to 1.0)",
        ge=0.0,
        le=1.0
    )
    language: str = Field(
        ...,
        description="Detected language: Hindi, English, or Unknown"
    )
    fraud_risk_explanation: str = Field(
        ...,
        description="Human-readable explanation of fraud risk assessment"
    )
    processing_time_ms: int = Field(
        ...,
        description="Processing time in milliseconds"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "label": "AI_GENERATED",
                "confidence": 0.8745,
                "language": "English",
                "fraud_risk_explanation": "High confidence AI-generated voice detected. Spectral patterns show synthetic characteristics.",
                "processing_time_ms": 1234
            }
        }


class ErrorResponse(BaseModel):
    """
    API error response model.
    """
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Detailed error message")
    processing_time_ms: Optional[int] = Field(None, description="Time until error")


class HealthResponse(BaseModel):
    """
    Health check response model.
    """
    status: str
    model_loaded: bool
    version: str


# Create API router
router = APIRouter()

# Global inference engine (loaded at startup)
inference_engine: Optional[InferenceEngine] = None


def get_inference_engine() -> InferenceEngine:
    """
    Dependency to get inference engine instance.
    
    Returns:
        InferenceEngine instance
        
    Raises:
        HTTPException: If model not loaded
    """
    if inference_engine is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "ModelNotLoaded",
                "message": "ML model not found. Train and upload model file to enable predictions.",
                "instructions": "1. Train locally: python train.py | 2. Upload model/voice_model.pkl to repository | 3. Redeploy"
            }
        )
    return inference_engine


@router.get("/", response_model=dict)
async def root():
    """
    Root endpoint - API information.
    """
    return {
        "name": "AI Voice Detection API",
        "version": "1.0.0",
        "description": "Detects AI-generated vs human voices for fraud prevention",
        "endpoints": {
            "POST /predict": "Analyze audio and detect AI-generated voice",
            "GET /health": "Health check endpoint",
            "GET /docs": "Interactive API documentation"
        }
    }


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    Always returns 200 OK, but indicates if model is loaded.
    """
    model_loaded = inference_engine is not None
    return {
        "status": "healthy" if model_loaded else "degraded",
        "model_loaded": model_loaded,
        "version": "1.0.0"
    }


@router.post(
    "/predict",
    response_model=PredictionResponse,
    responses={
        200: {"description": "Successful prediction"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        401: {"description": "Authentication failed"},
        503: {"model": ErrorResponse, "description": "Service unavailable"}
    }
)
async def predict_voice(
    request: PredictionRequest,
    api_key: str = Depends(api_key_auth.verify_api_key),
    engine: InferenceEngine = Depends(get_inference_engine)
):
    """
    Analyze audio file and detect if voice is AI-generated or human.
    
    **Authentication**: Requires Bearer token in Authorization header.
    
    **Process**:
    1. Download and validate audio from provided URL
    2. Extract MFCC and spectral features
    3. Classify using trained RandomForest model
    4. Return label, confidence, and fraud risk explanation
    
    **Response Time**: Typically < 2 seconds
    
    **Supported Audio Formats**: MP3, WAV, FLAC, OGG, M4A
    """
    start_time = time.time()
    
    try:
        # Validate URL format
        InputValidator.validate_url(request.audio_url)
        
        # Run inference
        result = engine.predict(request.audio_url)
        
        return PredictionResponse(**result)
        
    except ValidationError as e:
        processing_time = int((time.time() - start_time) * 1000)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "ValidationError",
                "detail": str(e),
                "processing_time_ms": processing_time
            }
        )
        
    except AudioDownloadError as e:
        processing_time = int((time.time() - start_time) * 1000)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "AudioDownloadError",
                "detail": str(e),
                "processing_time_ms": processing_time
            }
        )
        
    except Exception as e:
        processing_time = int((time.time() - start_time) * 1000)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalServerError",
                "detail": f"Unexpected error: {str(e)}",
                "processing_time_ms": processing_time
            }
        )


@router.get("/model/info")
async def model_info(
    api_key: str = Depends(api_key_auth.verify_api_key),
    engine: InferenceEngine = Depends(get_inference_engine)
):
    """
    Get information about the loaded ML model.
    
    Useful for debugging and verification during buildathon evaluation.
    """
    return engine.get_model_info()

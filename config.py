"""
Configuration Module for AI Voice Detection System

Centralized configuration management with environment variable support.
"""

import os
from typing import Optional
from pathlib import Path


class Config:
    """
    Application configuration with environment variable support.
    """
    
    # Project Paths
    PROJECT_ROOT = Path(__file__).parent
    MODEL_PATH = PROJECT_ROOT / "model" / "voice_model.pkl"
    DATA_DIR = PROJECT_ROOT / "data"
    
    # API Configuration
    API_KEY: str = os.getenv("API_KEY", "buildathon_demo_key_2026")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # Audio Processing Settings
    MAX_AUDIO_SIZE_MB: int = 50
    DOWNLOAD_TIMEOUT_SEC: int = 30
    TARGET_SAMPLE_RATE: int = 16000
    
    # Model Settings
    N_MFCC: int = 13
    N_FFT: int = 2048
    HOP_LENGTH: int = 512
    N_MELS: int = 128
    
    # ML Model Hyperparameters
    RANDOM_FOREST_N_ESTIMATORS: int = 200
    RANDOM_FOREST_MAX_DEPTH: int = 20
    RANDOM_FOREST_MIN_SAMPLES_SPLIT: int = 5
    
    # Deployment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment."""
        return cls.ENVIRONMENT.lower() == "production"
    
    @classmethod
    def validate_config(cls) -> bool:
        """
        Validate configuration before starting server.
        
        Returns:
            True if configuration is valid
        """
        issues = []
        
        # Check if model exists
        if not cls.MODEL_PATH.exists():
            issues.append(f"Model file not found: {cls.MODEL_PATH}")
        
        # Check if data directories exist
        if not cls.DATA_DIR.exists():
            issues.append(f"Data directory not found: {cls.DATA_DIR}")
        
        # Warn about default API key in production
        if cls.is_production() and cls.API_KEY == "buildathon_demo_key_2026":
            issues.append("WARNING: Using default API key in production!")
        
        if issues:
            print("\n⚠️  Configuration Issues:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        
        return True
    
    @classmethod
    def print_config(cls):
        """Print current configuration (for debugging)."""
        print("\n" + "=" * 60)
        print("CONFIGURATION")
        print("=" * 60)
        print(f"Environment: {cls.ENVIRONMENT}")
        print(f"Debug Mode: {cls.DEBUG}")
        print(f"API Host: {cls.HOST}:{cls.PORT}")
        print(f"Model Path: {cls.MODEL_PATH}")
        print(f"Data Directory: {cls.DATA_DIR}")
        print(f"Max Audio Size: {cls.MAX_AUDIO_SIZE_MB}MB")
        print(f"Sample Rate: {cls.TARGET_SAMPLE_RATE}Hz")
        print("=" * 60 + "\n")


# Create global config instance
config = Config()

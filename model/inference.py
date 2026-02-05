"""
Inference Pipeline for Real-time Voice Detection

This module provides a high-level interface for loading models
and running inference on audio URLs with timing and error handling.
"""

import time
import numpy as np
from typing import Dict
from .classifier import VoiceClassifier
from utils import AudioProcessor, FeatureExtractor, LanguageDetector


class InferenceEngine:
    """
    Complete inference pipeline for voice detection API.
    
    Pipeline Steps:
    1. Download and validate audio
    2. Extract acoustic features
    3. Run ML classification
    4. Generate explainable output
    """
    
    def __init__(self, model_path: str):
        """
        Initialize inference engine with trained model.
        
        Args:
            model_path: Path to saved model file
        """
        self.model = VoiceClassifier.load_model(model_path)
        self.audio_processor = AudioProcessor()
        self.feature_extractor = FeatureExtractor()
        print(f"✓ Inference engine initialized with model: {model_path}")
    
    def predict(self, audio_url: str) -> Dict:
        """
        Complete prediction pipeline with timing and error handling.
        
        Args:
            audio_url: URL to audio file
            
        Returns:
            Dictionary with prediction results
        """
        start_time = time.time()
        temp_path = None
        
        try:
            # Step 1: Download and preprocess audio
            audio, sr, temp_path = self.audio_processor.process_audio_from_url(
                audio_url
            )
            
            # Step 2: Extract features
            features = self.feature_extractor.extract_features(audio, sr)
            
            # Step 3: Run prediction
            label, confidence = self.model.predict(features)

            # 🔹 Safety threshold to reduce false AI accusation
            if label == "AI_GENERATED" and confidence < 0.85:
                label = "HUMAN"

            # Step 4: Detect language (lightweight heuristic)
            language = LanguageDetector.detect_language(temp_path)
            
            # Step 5: Generate fraud risk explanation
            fraud_explanation = self._generate_explanation(label, confidence)
            
            # Calculate processing time
            processing_time = int((time.time() - start_time) * 1000)

            
            return {
                'label': label,
                'confidence': round(confidence, 4),
                'language': language,
                'fraud_risk_explanation': fraud_explanation,
                'processing_time_ms': processing_time,
                'status': 'success'
            }
            
        finally:
            # Always cleanup temporary files
            if temp_path:
                self.audio_processor.cleanup(temp_path)
    
    def _generate_explanation(self, label: str, confidence: float) -> str:
        """
        Generate human-readable fraud risk explanation.
        
        Args:
            label: Predicted class label
            confidence: Prediction confidence (0-1)
            
        Returns:
            Explanation string
        """
        if label == "AI_GENERATED":
            if confidence > 0.85:
                return (
                    "High confidence AI-generated voice detected. "
                    "Spectral patterns show synthetic characteristics. "
                    "Recommend additional verification for fraud prevention."
                )
            elif confidence > 0.65:
                return (
                    "Likely AI-generated voice with moderate confidence. "
                    "Some synthetic markers detected. "
                    "Proceed with caution in sensitive contexts."
                )
            else:
                return (
                    "Possible AI-generated voice with low confidence. "
                    "Mixed signals detected. "
                    "Consider secondary verification methods."
                )
        else:  # HUMAN
            if confidence > 0.85:
                return (
                    "High confidence human voice detected. "
                    "Natural acoustic patterns consistent with human speech. "
                    "Low fraud risk based on audio analysis."
                )
            elif confidence > 0.65:
                return (
                    "Likely human voice with moderate confidence. "
                    "Predominantly natural speech characteristics. "
                    "Standard verification recommended."
                )
            else:
                return (
                    "Possible human voice with low confidence. "
                    "Ambiguous acoustic features. "
                    "Additional verification recommended for high-stakes decisions."
                )
    
    def get_model_info(self) -> Dict:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary with model metadata
        """
        return {
            'model_type': 'RandomForestClassifier',
            'n_estimators': self.model.model.n_estimators,
            'n_features': len(self.model.feature_names) if self.model.feature_names else None,
            'classes': self.model.class_names,
            'trained': self.model.trained
        }

"""
Model package for AI Voice Detection System
"""

from .classifier import VoiceClassifier
from .inference import InferenceEngine

__all__ = ['VoiceClassifier', 'InferenceEngine']

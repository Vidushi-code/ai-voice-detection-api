"""
Model Training Script for AI Voice Detection System

This script trains a RandomForest classifier to distinguish between
AI-generated and human voices using MFCC and spectral features.

Usage:
    python train.py

Requirements:
    - Place human voice samples in: data/human/
    - Place AI-generated samples in: data/ai/
    - Supported formats: MP3, WAV, FLAC, OGG
"""

import os
import sys
from pathlib import Path
import numpy as np
from glob import glob

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model.classifier import VoiceClassifier
from utils.feature_extractor import FeatureExtractor


def load_dataset(data_dir: str = "data") -> tuple:
    """
    Load audio dataset from directory structure.
    
    Expected structure:
        data/
        ├── human/
        │   ├── sample1.mp3
        │   ├── sample2.wav
        │   └── ...
        └── ai/
            ├── sample1.mp3
            ├── sample2.wav
            └── ...
    
    Args:
        data_dir: Root directory containing human/ and ai/ folders
        
    Returns:
        Tuple of (features, labels)
    """
    print("\n" + "=" * 60)
    print("LOADING DATASET")
    print("=" * 60)
    
    human_dir = os.path.join(data_dir, "human")
    ai_dir = os.path.join(data_dir, "ai")
    
    # Check if directories exist
    if not os.path.exists(human_dir):
        raise FileNotFoundError(
            f"Human voice directory not found: {human_dir}\n"
            f"Please create it and add audio samples."
        )
    
    if not os.path.exists(ai_dir):
        raise FileNotFoundError(
            f"AI voice directory not found: {ai_dir}\n"
            f"Please create it and add audio samples."
        )
    
    # Find all audio files
    audio_extensions = ['*.mp3', '*.wav', '*.flac', '*.ogg', '*.m4a']
    
    human_files = []
    for ext in audio_extensions:
        human_files.extend(glob(os.path.join(human_dir, ext)))
        human_files.extend(glob(os.path.join(human_dir, ext.upper())))
    
    ai_files = []
    for ext in audio_extensions:
        ai_files.extend(glob(os.path.join(ai_dir, ext)))
        ai_files.extend(glob(os.path.join(ai_dir, ext.upper())))
    
    print(f"\nFound audio files:")
    print(f"  Human voices: {len(human_files)}")
    print(f"  AI-generated: {len(ai_files)}")
    
    if len(human_files) == 0 or len(ai_files) == 0:
        raise ValueError(
            "Insufficient training data. Need at least 1 sample in each category.\n"
            f"Current: {len(human_files)} human, {len(ai_files)} AI\n\n"
            "To get started with sample data:\n"
            "1. Record or download human voice samples → data/human/\n"
            "2. Generate or download AI voice samples → data/ai/\n"
            "3. Aim for at least 50 samples per class for good performance"
        )
    
    # Extract features
    print("\nExtracting features from audio files...")
    print("(This may take a few minutes depending on dataset size)")
    
    feature_extractor = FeatureExtractor()
    
    # Process human voices
    print(f"\nProcessing {len(human_files)} human voice samples...")
    human_features = feature_extractor.extract_batch_features(human_files)
    human_labels = np.zeros(len(human_features), dtype=int)  # 0 = HUMAN
    
    # Process AI-generated voices
    print(f"Processing {len(ai_files)} AI-generated samples...")
    ai_features = feature_extractor.extract_batch_features(ai_files)
    ai_labels = np.ones(len(ai_features), dtype=int)  # 1 = AI_GENERATED
    
    # Combine datasets
    X = np.vstack([human_features, ai_features])
    y = np.hstack([human_labels, ai_labels])
    
    print(f"\nFeature extraction complete!")
    print(f"  Total samples: {len(X)}")
    print(f"  Features per sample: {X.shape[1]}")
    print(f"  Class distribution: {len(human_labels)} HUMAN, {len(ai_labels)} AI_GENERATED")
    
    # Get feature names for explainability
    feature_names = feature_extractor.get_feature_names()
    
    return X, y, feature_names


def main():
    """
    Main training pipeline.
    """
    print("\n" + "=" * 60)
    print("AI VOICE DETECTION - MODEL TRAINING")
    print("=" * 60)
    print("\nThis script will train a RandomForest classifier to detect")
    print("AI-generated voices vs. human voices.")
    print("\nFeature Engineering:")
    print("  - MFCC (Mel-Frequency Cepstral Coefficients)")
    print("  - Spectral Centroid, Rolloff, Bandwidth")
    print("  - Zero Crossing Rate")
    print("  - Chroma Features")
    
    try:
        # Load dataset
        X, y, feature_names = load_dataset()
        
        # Initialize and train classifier
        classifier = VoiceClassifier(
            n_estimators=200,
            max_depth=20,
            min_samples_split=5,
            random_state=42
        )
        
        # Train model
        metrics = classifier.train(X, y, feature_names)
        
        # Save model
        model_path = "model/voice_model.pkl"
        os.makedirs("model", exist_ok=True)
        classifier.save_model(model_path)
        
        # Summary
        print("\n" + "=" * 60)
        print("TRAINING SUMMARY")
        print("=" * 60)
        print(f"\n✓ Model trained successfully")
        print(f"✓ Test Accuracy: {metrics['test_accuracy']:.2%}")
        print(f"✓ CV Accuracy: {metrics['cv_mean']:.2%} (±{metrics['cv_std']*2:.2%})")
        print(f"✓ Model saved: {model_path}")
        print(f"\n✓ Ready for deployment!")
        print("\nNext steps:")
        print("  1. Test the model: python -m pytest tests/")
        print("  2. Start the API: python main.py")
        print("  3. Test with curl or Postman")
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: {e}")
        print("\nQuick Start Guide:")
        print("=" * 60)
        print("1. Create data directories:")
        print("   mkdir -p data/human data/ai")
        print("\n2. Add training samples:")
        print("   - Place human voice recordings in data/human/")
        print("   - Place AI-generated voices in data/ai/")
        print("   - Minimum: 10 samples per class")
        print("   - Recommended: 50+ samples per class")
        print("\n3. Sample sources:")
        print("   - Human: Record yourself or use public speech datasets")
        print("   - AI: Use ElevenLabs, Murf.ai, or other TTS services")
        print("\n4. Run training again: python train.py")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ TRAINING FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

"""
Voice Classification Model Training and Inference

This module handles ML model training, evaluation, and inference
for AI-generated vs Human voice detection.
"""

import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
from typing import Tuple, Dict, Optional
from pathlib import Path
import json


class VoiceClassifier:
    """
    RandomForest-based classifier for detecting AI-generated voices.
    
    Why RandomForest?
    -----------------
    1. Fast inference (<100ms)
    2. Good explainability (feature importance)
    3. Robust to overfitting
    4. No GPU required
    5. Works well with limited training data
    """
    
    def __init__(
    self,
    n_estimators: int = 120,
    max_depth: int = 12,
    min_samples_split: int = 4,
    min_samples_leaf: int = 2,
    random_state: int = 42,
    ):

        """
        Initialize RandomForest classifier.
        
        Args:
            n_estimators: Number of trees in the forest
            max_depth: Maximum depth of trees
            min_samples_split: Minimum samples required to split
            random_state: Random seed for reproducibility
        """
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            random_state=random_state,
            n_jobs=-1,  # Use all CPU cores
            class_weight='balanced'  # Handle class imbalance
        )
        self.feature_names = None
        self.class_names = ['HUMAN', 'AI_GENERATED']
        self.trained = False
    
    def train(
        self,
        X: np.ndarray,
        y: np.ndarray,
        feature_names: Optional[list] = None
    ) -> Dict[str, float]:
        """
        Train the classifier with cross-validation.
        
        Args:
            X: Feature matrix (n_samples x n_features)
            y: Labels (0 = HUMAN, 1 = AI_GENERATED)
            feature_names: Optional list of feature names
            
        Returns:
            Dictionary with training metrics
        """
        print("=" * 60)
        print("TRAINING AI VOICE DETECTION MODEL")
        print("=" * 60)
        
        self.feature_names = feature_names
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"\nDataset Split:")
        print(f"  Training samples: {len(X_train)}")
        print(f"  Testing samples: {len(X_test)}")
        print(f"  Features: {X.shape[1]}")
        
        # Cross-validation on training set
        print("\nPerforming 5-Fold Cross-Validation...")
        cv_scores = cross_val_score(
            self.model, X_train, y_train, cv=5, scoring='accuracy'
        )
        print(f"  CV Scores: {cv_scores}")
        print(f"  CV Mean: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        # Train on full training set
        print("\nTraining final model...")
        self.model.fit(X_train, y_train)
        self.trained = True
        
        # Evaluate on test set
        print("\nEvaluating on test set...")
        y_pred = self.model.predict(X_test)
        test_accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\nTest Accuracy: {test_accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(
            y_test, y_pred,
            target_names=self.class_names,
            digits=4
        ))
        
        print("\nConfusion Matrix:")
        cm = confusion_matrix(y_test, y_pred)
        print(f"                Predicted")
        print(f"              HUMAN  AI_GEN")
        print(f"Actual HUMAN    {cm[0][0]:4d}   {cm[0][1]:4d}")
        print(f"       AI_GEN   {cm[1][0]:4d}   {cm[1][1]:4d}")
        
        # Feature importance
        if feature_names:
            print("\nTop 10 Most Important Features:")
            importances = self.model.feature_importances_
            indices = np.argsort(importances)[::-1][:10]
            for i, idx in enumerate(indices, 1):
                print(f"  {i}. {feature_names[idx]}: {importances[idx]:.4f}")
        
        print("\n" + "=" * 60)
        print("TRAINING COMPLETE")
        print("=" * 60)
        
        return {
            'test_accuracy': float(test_accuracy),
            'cv_mean': float(cv_scores.mean()),
            'cv_std': float(cv_scores.std())
        }
    
    def predict(
        self,
        features: np.ndarray
    ) -> Tuple[str, float]:
        """
        Predict class and confidence for audio features.
        
        Args:
            features: Feature vector (1D array)
            
        Returns:
            Tuple of (label, confidence)
        """
        if not self.trained:
            raise RuntimeError("Model not trained. Load a trained model first.")
        
        # Reshape for single prediction
        if len(features.shape) == 1:
            features = features.reshape(1, -1)
        
        # Get prediction and probability
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        
        label = self.class_names[prediction]
        confidence = float(probabilities[prediction])
        
        return label, confidence
    
    def save_model(self, model_path: str):
        """
        Save trained model to disk.
        
        Args:
            model_path: Path to save model file
        """
        if not self.trained:
            raise RuntimeError("Cannot save untrained model")
        
        model_data = {
            'model': self.model,
            'feature_names': self.feature_names,
            'class_names': self.class_names,
            'trained': self.trained
        }
        
        joblib.dump(model_data, model_path)
        print(f"\nModel saved to: {model_path}")
    
    @classmethod
    def load_model(cls, model_path: str) -> 'VoiceClassifier':
        """
        Load trained model from disk.
        
        Args:
            model_path: Path to model file
            
        Returns:
            Loaded VoiceClassifier instance
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        model_data = joblib.load(model_path)
        
        classifier = cls()
        classifier.model = model_data['model']
        classifier.feature_names = model_data['feature_names']
        classifier.class_names = model_data['class_names']
        classifier.trained = model_data['trained']
        
        return classifier
    
    def get_feature_importance(self, top_n: int = 20) -> Dict[str, float]:
        """
        Get feature importance scores for explainability.
        
        Args:
            top_n: Number of top features to return
            
        Returns:
            Dictionary mapping feature names to importance scores
        """
        if not self.trained or not self.feature_names:
            return {}
        
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1][:top_n]
        
        return {
            self.feature_names[idx]: float(importances[idx])
            for idx in indices
        }

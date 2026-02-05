"""
Audio Feature Extraction using MFCC and Spectral Analysis

This module extracts acoustic features that distinguish AI-generated voices
from human voices. MFCCs capture the spectral envelope characteristics that
are different in synthetic vs. natural speech.
"""

import numpy as np
import librosa
from typing import Dict, List


class FeatureExtractor:
    """
    Extracts MFCC and spectral features for voice classification.
    
    Why MFCC?
    ---------
    Mel-Frequency Cepstral Coefficients (MFCCs) represent the short-term 
    power spectrum of sound on a mel scale (mimicking human hearing).
    
    AI-generated voices often show:
    - More uniform spectral patterns
    - Different harmonic structures
    - Anomalies in high-frequency content
    - Less natural variation in prosody
    """
    
    def __init__(
        self,
        n_mfcc: int = 13,
        n_fft: int = 2048,
        hop_length: int = 512,
        n_mels: int = 128
    ):
        """
        Initialize feature extractor with audio processing parameters.
        
        Args:
            n_mfcc: Number of MFCC coefficients (13 is standard)
            n_fft: FFT window size
            hop_length: Number of samples between successive frames
            n_mels: Number of Mel bands
        """
        self.n_mfcc = n_mfcc
        self.n_fft = n_fft
        self.hop_length = hop_length
        self.n_mels = n_mels
    
    def extract_features(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """
        Extract comprehensive feature vector from audio.
        
        Feature Components:
        -------------------
        1. MFCC statistics (mean, std, min, max) - 52 features
        2. Spectral centroid statistics - 4 features
        3. Spectral rolloff statistics - 4 features
        4. Zero crossing rate statistics - 4 features
        5. Spectral bandwidth statistics - 4 features
        6. Chroma features statistics - 48 features
        
        Total: 116 features per audio sample
        
        Args:
            audio: Audio waveform (mono, normalized)
            sr: Sample rate
            
        Returns:
            1D numpy array of extracted features
        """
        features = []
        
        # 1. Extract MFCCs - Most important for voice characteristics
        mfcc = librosa.feature.mfcc(
            y=audio,
            sr=sr,
            n_mfcc=self.n_mfcc,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )
        features.extend(self._compute_statistics(mfcc))
        
        # 2. Spectral Centroid - Center of mass of spectrum
        # AI voices may have different spectral distribution
        spectral_centroid = librosa.feature.spectral_centroid(
            y=audio,
            sr=sr,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )
        features.extend(self._compute_statistics(spectral_centroid))
        
        # 3. Spectral Rolloff - Frequency below which 85% of energy is contained
        spectral_rolloff = librosa.feature.spectral_rolloff(
            y=audio,
            sr=sr,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )
        features.extend(self._compute_statistics(spectral_rolloff))
        
        # 4. Zero Crossing Rate - Rate of sign changes
        # Useful for detecting synthetic artifacts
        zcr = librosa.feature.zero_crossing_rate(
            y=audio,
            frame_length=self.n_fft,
            hop_length=self.hop_length
        )
        features.extend(self._compute_statistics(zcr))
        
        # 5. Spectral Bandwidth - Width of frequency spectrum
        spectral_bandwidth = librosa.feature.spectral_bandwidth(
            y=audio,
            sr=sr,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )
        features.extend(self._compute_statistics(spectral_bandwidth))
        
        # 6. Chroma Features - Pitch class distribution
        # AI may have unnatural pitch patterns
        chroma = librosa.feature.chroma_stft(
            y=audio,
            sr=sr,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )
        features.extend(self._compute_statistics(chroma))
        
        return np.array(features)
    
    def _compute_statistics(self, feature_matrix: np.ndarray) -> List[float]:
        """
        Compute statistical summaries of temporal features.
        
        For each feature dimension, compute:
        - Mean: Average value over time
        - Std: Variation over time
        - Min: Minimum value
        - Max: Maximum value
        
        Args:
            feature_matrix: 2D array (features x time)
            
        Returns:
            List of statistical values
        """
        stats = []
        for row in feature_matrix:
            stats.extend([
                float(np.mean(row)),
                float(np.std(row)),
                float(np.min(row)),
                float(np.max(row))
            ])
        return stats
    
    def get_feature_names(self) -> List[str]:
        """
        Get human-readable names for all extracted features.
        Useful for model explainability.
        
        Returns:
            List of feature names
        """
        names = []
        
        # MFCC features
        for i in range(self.n_mfcc):
            names.extend([
                f'mfcc_{i}_mean',
                f'mfcc_{i}_std',
                f'mfcc_{i}_min',
                f'mfcc_{i}_max'
            ])
        
        # Spectral features
        for feature_name in ['spectral_centroid', 'spectral_rolloff', 
                             'zero_crossing_rate', 'spectral_bandwidth']:
            names.extend([
                f'{feature_name}_mean',
                f'{feature_name}_std',
                f'{feature_name}_min',
                f'{feature_name}_max'
            ])
        
        # Chroma features
        for i in range(12):  # 12 pitch classes
            names.extend([
                f'chroma_{i}_mean',
                f'chroma_{i}_std',
                f'chroma_{i}_min',
                f'chroma_{i}_max'
            ])
        
        return names
    
    def extract_batch_features(
        self,
        audio_files: List[str],
        sr: int = 16000
    ) -> np.ndarray:
        """
        Extract features from multiple audio files (used in training).
        
        Args:
            audio_files: List of file paths
            sr: Sample rate
            
        Returns:
            2D array of features (n_samples x n_features)
        """
        features_list = []
        
        for file_path in audio_files:
            try:
                # Load audio
                audio, _ = librosa.load(file_path, sr=sr, mono=True)
                
                # Extract features
                features = self.extract_features(audio, sr)
                features_list.append(features)
                
            except Exception as e:
                print(f"Warning: Failed to process {file_path}: {e}")
                continue
        
        return np.array(features_list)

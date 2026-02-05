"""
Audio Download and Preprocessing Utilities

This module handles secure audio download, validation, and preprocessing
for the voice detection system. Supports MP3, WAV, and common audio formats.
"""

import os
import tempfile
import requests
from typing import Tuple, Optional
import librosa
import numpy as np
from pathlib import Path
import hashlib
import time


class AudioDownloadError(Exception):
    """Raised when audio download or validation fails"""
    pass


class AudioProcessor:
    """
    Handles audio file download, validation, and preprocessing
    with security checks and error handling.
    """
    
    SUPPORTED_FORMATS = ['.mp3', '.wav', '.flac', '.ogg', '.m4a']
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB limit
    DOWNLOAD_TIMEOUT = 30  # seconds
    TARGET_SAMPLE_RATE = 16000  # Standard for speech processing
    
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
    
    def download_audio(self, url: str) -> str:
        """
        Securely download audio file from URL with validation.
        
        Args:
            url: HTTP/HTTPS URL to audio file
            
        Returns:
            str: Path to downloaded temporary file
            
        Raises:
            AudioDownloadError: If download fails or file is invalid
        """
        if not url.startswith(('http://', 'https://')):
            raise AudioDownloadError("Invalid URL: must use http or https protocol")
        
        try:
            # Generate unique filename to avoid collisions
            file_hash = hashlib.md5(f"{url}{time.time()}".encode()).hexdigest()
            temp_path = os.path.join(self.temp_dir, f"audio_{file_hash}.tmp")
            
            # Download with timeout and size limit
            response = requests.get(
                url,
                stream=True,
                timeout=self.DOWNLOAD_TIMEOUT,
                headers={'User-Agent': 'AI-Voice-Detector/1.0'}
            )
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('content-type', '').lower()
            if not any(fmt in content_type for fmt in ['audio', 'mpeg', 'wav', 'ogg', 'flac']):
                # Still allow if we can't determine - will validate with librosa
                pass
            
            # Download with size check
            total_size = 0
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        total_size += len(chunk)
                        if total_size > self.MAX_FILE_SIZE:
                            os.remove(temp_path)
                            raise AudioDownloadError(
                                f"File too large: exceeds {self.MAX_FILE_SIZE / (1024*1024)}MB limit"
                            )
                        f.write(chunk)
            
            if total_size == 0:
                os.remove(temp_path)
                raise AudioDownloadError("Downloaded file is empty")
            
            return temp_path
            
        except requests.RequestException as e:
            raise AudioDownloadError(f"Download failed: {str(e)}")
        except Exception as e:
            raise AudioDownloadError(f"Unexpected error during download: {str(e)}")
    
    def load_and_preprocess(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        Load audio file and preprocess for feature extraction.
        
        This method:
        1. Loads audio using librosa
        2. Resamples to standard 16kHz
        3. Converts to mono
        4. Normalizes amplitude
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Tuple of (audio_data, sample_rate)
            
        Raises:
            AudioDownloadError: If file cannot be loaded or is corrupted
        """
        try:
            # Load audio file - librosa handles multiple formats
            audio, sr = librosa.load(
                file_path,
                sr=self.TARGET_SAMPLE_RATE,  # Resample to 16kHz
                mono=True,  # Convert to mono
                duration=60  # Limit to 60 seconds for processing efficiency
            )
            
            # Validate audio data
            if len(audio) == 0:
                raise AudioDownloadError("Audio file is empty or corrupted")
            
            if len(audio) < sr * 0.5:  # Less than 0.5 seconds
                raise AudioDownloadError("Audio too short: minimum 0.5 seconds required")
            
            # Normalize audio to [-1, 1] range
            audio = self._normalize_audio(audio)
            
            return audio, sr
            
        except Exception as e:
            raise AudioDownloadError(f"Failed to load audio: {str(e)}")
    
    def _normalize_audio(self, audio: np.ndarray) -> np.ndarray:
        """
        Normalize audio amplitude to [-1, 1] range.
        
        Args:
            audio: Raw audio waveform
            
        Returns:
            Normalized audio array
        """
        max_val = np.abs(audio).max()
        if max_val > 0:
            audio = audio / max_val
        return audio
    
    def cleanup(self, file_path: str):
        """
        Remove temporary audio file.
        
        Args:
            file_path: Path to temporary file
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            # Silent fail - temp files will be cleaned by OS eventually
            pass
    
    def process_audio_from_url(self, url: str) -> Tuple[np.ndarray, int, str]:
        """
        Complete pipeline: download, validate, and preprocess audio.
        
        Args:
            url: Audio file URL
            
        Returns:
            Tuple of (audio_data, sample_rate, temp_file_path)
            
        Raises:
            AudioDownloadError: If any step fails
        """
        temp_path = None
        try:
            # Download audio
            temp_path = self.download_audio(url)
            
            # Load and preprocess
            audio, sr = self.load_and_preprocess(temp_path)
            
            return audio, sr, temp_path
            
        except Exception as e:
            # Cleanup on failure
            if temp_path:
                self.cleanup(temp_path)
            raise

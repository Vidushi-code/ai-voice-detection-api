"""
Input Validation and Language Detection Utilities

This module provides validation functions for API inputs and 
lightweight language detection for multi-language support.
"""

import re
from typing import Dict, Optional
from urllib.parse import urlparse


class ValidationError(Exception):
    """Raised when validation fails"""
    pass


class InputValidator:
    """
    Validates API inputs and provides security checks.
    """
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate URL format and security.
        
        Args:
            url: URL string to validate
            
        Returns:
            True if valid
            
        Raises:
            ValidationError: If URL is invalid or insecure
        """
        if not url or not isinstance(url, str):
            raise ValidationError("URL must be a non-empty string")
        
        # Check URL format
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                raise ValidationError("Invalid URL format")
            
            if result.scheme not in ['http', 'https']:
                raise ValidationError("URL must use HTTP or HTTPS protocol")
            
        except Exception as e:
            raise ValidationError(f"Invalid URL: {str(e)}")
        
        # Security: Block common dangerous patterns
        dangerous_patterns = [
            'localhost',
            '127.0.0.1',
            '0.0.0.0',
            '192.168.',
            '10.',
            '172.16.',
            'file://',
            'ftp://'
        ]
        
        url_lower = url.lower()
        for pattern in dangerous_patterns:
            if pattern in url_lower:
                raise ValidationError(
                    f"Security: Cannot access local/internal resources"
                )
        
        return True
    
    @staticmethod
    def validate_api_key(api_key: Optional[str], expected_key: str) -> bool:
        """
        Validate API key for authentication.
        
        Args:
            api_key: Provided API key
            expected_key: Expected API key from config
            
        Returns:
            True if valid
            
        Raises:
            ValidationError: If key is invalid
        """
        if not api_key:
            raise ValidationError("API key is required")
        
        if api_key != expected_key:
            raise ValidationError("Invalid API key")
        
        return True


class LanguageDetector:
    """
    Lightweight language detection for Hindi/English/Unknown.
    
    Uses character set heuristics rather than heavy NLP models
    to maintain fast inference time.
    """
    
    # Devanagari Unicode range for Hindi
    HINDI_RANGE = (0x0900, 0x097F)
    
    @classmethod
    def detect_language(cls, audio_path: str) -> str:
        """
        Detect language from audio file name or metadata.
        
        Note: This is a lightweight heuristic. For production deployment
        with language-specific models, integrate a proper language 
        identification system (e.g., langid, speechbrain).
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            "Hindi", "English", or "Unknown"
        """
        # Simple heuristic: check file path for language indicators
        path_lower = audio_path.lower()
        
        if any(indicator in path_lower for indicator in ['hindi', 'hi_', '_hi', 'hin']):
            return "Hindi"
        elif any(indicator in path_lower for indicator in ['english', 'en_', '_en', 'eng']):
            return "English"
        else:
            return "Unknown"
    
    @classmethod
    def detect_from_text(cls, text: str) -> str:
        """
        Detect language from text (for future transcript-based detection).
        
        Args:
            text: Text string to analyze
            
        Returns:
            "Hindi", "English", or "Unknown"
        """
        if not text:
            return "Unknown"
        
        # Count Devanagari characters
        hindi_chars = sum(
            1 for char in text 
            if cls.HINDI_RANGE[0] <= ord(char) <= cls.HINDI_RANGE[1]
        )
        
        # Count English characters
        english_chars = sum(1 for char in text if char.isalpha() and ord(char) < 128)
        
        total_chars = hindi_chars + english_chars
        
        if total_chars == 0:
            return "Unknown"
        
        hindi_ratio = hindi_chars / total_chars
        
        if hindi_ratio > 0.3:
            return "Hindi"
        elif english_chars > hindi_chars:
            return "English"
        else:
            return "Unknown"


def sanitize_string(input_str: str, max_length: int = 500) -> str:
    """
    Sanitize user input string for logging/display.
    
    Args:
        input_str: Input string
        max_length: Maximum allowed length
        
    Returns:
        Sanitized string
    """
    if not input_str:
        return ""
    
    # Truncate
    sanitized = input_str[:max_length]
    
    # Remove control characters
    sanitized = re.sub(r'[\x00-\x1F\x7F]', '', sanitized)
    
    return sanitized

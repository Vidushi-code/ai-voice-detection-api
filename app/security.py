"""
Security and Authentication Module

Handles API key authentication and rate limiting for production deployment.
"""

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import os


# Security scheme for Bearer token
security_scheme = HTTPBearer()


class APIKeyAuth:
    """
    API Key authentication handler.
    
    In production, use environment variable for API key.
    For buildathon demo, a default key is provided.
    """
    
    def __init__(self):
        # Load API key from environment or use default
        self.api_key = os.getenv("API_KEY", "buildathon_demo_key_2026")
        
        if self.api_key == "buildathon_demo_key_2026":
            print("\n⚠️  WARNING: Using default API key. Set API_KEY environment variable for production.")
    
    def verify_api_key(
        self,
        credentials: HTTPAuthorizationCredentials = Security(security_scheme)
    ) -> str:
        """
        Verify API key from Authorization header.
        
        Args:
            credentials: Bearer token from request header
            
        Returns:
            API key if valid
            
        Raises:
            HTTPException: If authentication fails
        """
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        provided_key = credentials.credentials
        
        if provided_key != self.api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return provided_key


# Global instance
api_key_auth = APIKeyAuth()

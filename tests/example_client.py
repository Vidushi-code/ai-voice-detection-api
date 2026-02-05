"""
Sample Python client for AI Voice Detection API

This demonstrates how to integrate the API into your application.
"""

import requests
from typing import Dict, Optional


class VoiceDetectionClient:
    """
    Python client for AI Voice Detection API.
    """
    
    def __init__(self, api_url: str, api_key: str):
        """
        Initialize client.
        
        Args:
            api_url: Base URL of API (e.g., "https://api.example.com")
            api_key: Your API key
        """
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def analyze_audio(self, audio_url: str) -> Dict:
        """
        Analyze audio file for AI-generated voice detection.
        
        Args:
            audio_url: HTTP/HTTPS URL to audio file
            
        Returns:
            Dictionary with prediction results
            
        Raises:
            requests.HTTPError: If API request fails
        """
        response = requests.post(
            f"{self.api_url}/predict",
            headers=self.headers,
            json={"audio_url": audio_url}
        )
        response.raise_for_status()
        return response.json()
    
    def is_ai_generated(self, audio_url: str, threshold: float = 0.7) -> bool:
        """
        Simple helper to check if voice is AI-generated.
        
        Args:
            audio_url: HTTP/HTTPS URL to audio file
            threshold: Confidence threshold (0-1)
            
        Returns:
            True if AI-generated with confidence > threshold
        """
        result = self.analyze_audio(audio_url)
        return result['label'] == 'AI_GENERATED' and result['confidence'] >= threshold
    
    def health_check(self) -> bool:
        """
        Check if API is healthy.
        
        Returns:
            True if API is healthy
        """
        try:
            response = requests.get(f"{self.api_url}/health")
            data = response.json()
            return data.get('status') == 'healthy'
        except:
            return False


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = VoiceDetectionClient(
        api_url="http://localhost:8000",
        api_key="buildathon_demo_key_2026"
    )
    
    # Check health
    if not client.health_check():
        print("❌ API is not available")
        exit(1)
    
    print("✓ API is healthy\n")
    
    # Example: Analyze audio
    test_url = "https://www.kozco.com/tech/piano2.wav"
    
    try:
        print(f"Analyzing: {test_url}\n")
        result = client.analyze_audio(test_url)
        
        print("Results:")
        print(f"  Label: {result['label']}")
        print(f"  Confidence: {result['confidence']:.2%}")
        print(f"  Language: {result['language']}")
        print(f"  Processing Time: {result['processing_time_ms']}ms")
        print(f"\nExplanation:")
        print(f"  {result['fraud_risk_explanation']}")
        
        # Simple fraud check
        if client.is_ai_generated(test_url, threshold=0.7):
            print("\n⚠️  HIGH FRAUD RISK: AI-generated voice detected!")
        else:
            print("\n✓ Low fraud risk: Likely human voice")
            
    except requests.HTTPError as e:
        print(f"❌ API Error: {e}")
        print(f"Response: {e.response.text}")

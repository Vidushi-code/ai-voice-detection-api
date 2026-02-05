"""
API Testing Script

This script tests the AI Voice Detection API with various scenarios.

Usage:
    python test_api.py
"""

import requests
import time
import json
from typing import Dict, List


class APITester:
    """
    Test client for Voice Detection API.
    """
    
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = "buildathon_demo_key_2026"):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def test_health(self):
        """Test health check endpoint."""
        print("\n" + "=" * 60)
        print("TEST: Health Check")
        print("=" * 60)
        
        try:
            response = requests.get(f"{self.base_url}/health")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def test_predict(self, audio_url: str, expected_label: str = None):
        """Test prediction endpoint with an audio URL."""
        print("\n" + "=" * 60)
        print(f"TEST: Predict - {audio_url}")
        print("=" * 60)
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/predict",
                headers=self.headers,
                json={"audio_url": audio_url}
            )
            elapsed = time.time() - start_time
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Time: {elapsed:.2f}s")
            
            if response.status_code == 200:
                result = response.json()
                print(f"\nResult:")
                print(f"  Label: {result['label']}")
                print(f"  Confidence: {result['confidence']:.4f}")
                print(f"  Language: {result['language']}")
                print(f"  Processing Time: {result['processing_time_ms']}ms")
                print(f"  Explanation: {result['fraud_risk_explanation']}")
                
                if expected_label:
                    match = result['label'] == expected_label
                    print(f"\n  Expected: {expected_label}")
                    print(f"  Match: {'✓' if match else '✗'}")
                    return match
                return True
            else:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def test_invalid_url(self):
        """Test with invalid URL."""
        print("\n" + "=" * 60)
        print("TEST: Invalid URL")
        print("=" * 60)
        
        try:
            response = requests.post(
                f"{self.base_url}/predict",
                headers=self.headers,
                json={"audio_url": "not-a-valid-url"}
            )
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return response.status_code == 400
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def test_unauthorized(self):
        """Test without API key."""
        print("\n" + "=" * 60)
        print("TEST: Unauthorized Access")
        print("=" * 60)
        
        try:
            response = requests.post(
                f"{self.base_url}/predict",
                json={"audio_url": "https://example.com/test.mp3"}
            )
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return response.status_code == 401
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def test_model_info(self):
        """Test model info endpoint."""
        print("\n" + "=" * 60)
        print("TEST: Model Info")
        print("=" * 60)
        
        try:
            response = requests.get(
                f"{self.base_url}/model/info",
                headers=self.headers
            )
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def run_all_tests(self, test_audio_urls: List[Dict] = None):
        """Run all tests."""
        print("\n" + "=" * 60)
        print("AI VOICE DETECTION API - TEST SUITE")
        print("=" * 60)
        print(f"Base URL: {self.base_url}")
        print(f"API Key: {self.api_key}")
        
        results = []
        
        # Test 1: Health Check
        results.append(("Health Check", self.test_health()))
        
        # Test 2: Model Info
        results.append(("Model Info", self.test_model_info()))
        
        # Test 3: Unauthorized Access
        results.append(("Unauthorized Access", self.test_unauthorized()))
        
        # Test 4: Invalid URL
        results.append(("Invalid URL", self.test_invalid_url()))
        
        # Test 5: Prediction with sample URLs
        if test_audio_urls:
            for i, test_case in enumerate(test_audio_urls, 1):
                url = test_case.get("url")
                expected = test_case.get("expected_label")
                result = self.test_predict(url, expected)
                results.append((f"Prediction Test {i}", result))
        
        # Summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total = len(results)
        passed = sum(1 for _, result in results if result)
        failed = total - passed
        
        for test_name, result in results:
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"{status} - {test_name}")
        
        print(f"\nTotal: {total} | Passed: {passed} | Failed: {failed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        return passed == total


def main():
    """
    Main test execution.
    """
    tester = APITester()
    
    # Sample test URLs (replace with actual audio URLs for testing)
    test_cases = [
        {
            "url": "https://www.kozco.com/tech/piano2.wav",
            "expected_label": None  # Set to "HUMAN" or "AI_GENERATED" if known
        }
    ]
    
    # Note: For comprehensive testing, add more test cases with known labels
    print("\n⚠️  Note: Replace test URLs with actual human/AI voice samples")
    print("for comprehensive testing.\n")
    
    success = tester.run_all_tests(test_cases)
    
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed. Check output above.")
    
    return 0 if success else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())

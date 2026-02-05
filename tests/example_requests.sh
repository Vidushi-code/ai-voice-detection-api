# Example cURL requests for API testing

# 1. Health Check (no auth required)
curl http://localhost:8000/health

# 2. Predict with audio URL
curl -X POST "http://localhost:8000/predict" \
  -H "Authorization: Bearer buildathon_demo_key_2026" \
  -H "Content-Type: application/json" \
  -d '{"audio_url": "https://www.kozco.com/tech/piano2.wav"}'

# 3. Get model information
curl -X GET "http://localhost:8000/model/info" \
  -H "Authorization: Bearer buildathon_demo_key_2026"

# 4. Test with invalid URL (expect 400 error)
curl -X POST "http://localhost:8000/predict" \
  -H "Authorization: Bearer buildathon_demo_key_2026" \
  -H "Content-Type: application/json" \
  -d '{"audio_url": "not-a-valid-url"}'

# 5. Test without authentication (expect 401 error)
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"audio_url": "https://example.com/audio.mp3"}'

# 6. Root endpoint
curl http://localhost:8000/

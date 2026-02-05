# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Install Dependencies (2 minutes)

```bash
# Navigate to project
cd ai-impact

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Upgrade pip and install build tools (IMPORTANT!)
python -m pip install --upgrade pip setuptools wheel

# Install packages
pip install -r requirements.txt
```

### Step 2: Prepare Training Data (1 minute)

```bash
# Create directories
mkdir -p data/human data/ai
```

**Quick Test Data:**
- Record 5 voice memos on your phone → Save to `data/human/`
- Go to [ElevenLabs](https://elevenlabs.io/) → Generate 5 samples → Save to `data/ai/`

### Step 3: Train Model (1 minute)

```bash
python train.py
```

Wait for training to complete. You should see:
```
✓ Model saved to: model/voice_model.pkl
✓ Ready for deployment!
```

### Step 4: Start API (30 seconds)

```bash
python main.py
```

Server starts at `http://localhost:8000`

### Step 5: Test It (30 seconds)

Open browser: `http://localhost:8000/docs`

Or use cURL:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Authorization: Bearer buildathon_demo_key_2026" \
  -H "Content-Type: application/json" \
  -d '{"audio_url": "https://www.kozco.com/tech/piano2.wav"}'
```

---

## 🎯 Common Issues

### Issue: `ModuleNotFoundError: No module named 'librosa'`
**Solution:** 
```bash
pip install -r requirements.txt
```

### Issue: `Model file not found`
**Solution:**
```bash
python train.py
```

### Issue: `No audio files found in data/`
**Solution:**
Add audio files to `data/human/` and `data/ai/`, then run `python train.py`

### Issue: `Failed to download audio`
**Solution:**
Check audio URL is:
- Publicly accessible
- Valid HTTP/HTTPS URL
- Not localhost or internal IP

---

## 📦 What's Included

```
ai-impact/
├── app/                    # FastAPI application
│   ├── api.py             # API routes
│   ├── security.py        # Authentication
│   └── __init__.py
├── model/                  # ML model
│   ├── classifier.py      # RandomForest trainer
│   ├── inference.py       # Prediction engine
│   └── __init__.py
├── utils/                  # Utilities
│   ├── audio_utils.py     # Audio download/preprocessing
│   ├── feature_extractor.py  # MFCC extraction
│   ├── validation.py      # Input validation
│   └── __init__.py
├── data/                   # Training data
│   ├── human/             # Human voice samples
│   └── ai/                # AI-generated samples
├── tests/                  # Testing scripts
│   ├── test_api.py        # API tests
│   ├── example_client.py  # Python client
│   └── example_requests.sh  # cURL examples
├── main.py                 # Application entry point
├── train.py                # Model training script
├── config.py               # Configuration
├── requirements.txt        # Dependencies
├── README.md               # Full documentation
├── DEPLOYMENT.md           # Deployment guide
├── PRESENTATION.md         # Presentation guide
└── .env.example            # Environment template
```

---

## 🧪 Quick Tests

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```

Expected:
```json
{"status": "healthy", "model_loaded": true, "version": "1.0.0"}
```

### Test 2: Prediction
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Authorization: Bearer buildathon_demo_key_2026" \
  -H "Content-Type: application/json" \
  -d '{"audio_url": "YOUR_AUDIO_URL_HERE"}'
```

Expected:
```json
{
  "label": "HUMAN",
  "confidence": 0.87,
  "language": "English",
  "fraud_risk_explanation": "...",
  "processing_time_ms": 1234
}
```

### Test 3: Interactive Docs
Open browser: `http://localhost:8000/docs`

Click "Try it out" on `/predict` endpoint!

---

## 🎓 Learning Resources

### Understanding MFCCs
- [What are MFCCs?](https://en.wikipedia.org/wiki/Mel-frequency_cepstrum)
- [Librosa MFCC Tutorial](https://librosa.org/doc/main/generated/librosa.feature.mfcc.html)

### FastAPI
- [Official Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [API Documentation](https://fastapi.tiangolo.com/)

### RandomForest
- [Scikit-learn Guide](https://scikit-learn.org/stable/modules/ensemble.html#forest)

---

## 💡 Next Steps

1. **Improve Model:** Add more training data (50+ samples per class)
2. **Deploy:** Follow [DEPLOYMENT.md](DEPLOYMENT.md) for cloud deployment
3. **Customize:** Adjust model parameters in `config.py`
4. **Test:** Run comprehensive tests with `python tests/test_api.py`
5. **Present:** Use [PRESENTATION.md](PRESENTATION.md) for hackathon pitch

---

## 📞 Need Help?

- Check [README.md](README.md) for detailed documentation
- See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment issues
- Review code comments - every module is documented!

---

**Ready to win the hackathon? Let's go! 🏆**

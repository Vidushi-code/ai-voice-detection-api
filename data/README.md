# AI Voice Detection Data Directory

This directory contains training data for the AI voice detection model.

## Structure

```
data/
├── human/          # Human voice recordings
│   ├── sample1.mp3
│   ├── sample2.wav
│   └── ...
└── ai/             # AI-generated voice samples
    ├── sample1.mp3
    ├── sample2.wav
    └── ...
```

## Data Collection Guidelines

### Human Voice Samples

**Recommended sources:**
1. Record yourself speaking (at least 30 seconds per sample)
2. Ask friends/family to contribute recordings
3. Use public datasets:
   - [Common Voice](https://commonvoice.mozilla.org/)
   - [LibriSpeech](https://www.openslr.org/12/)
   - [VCTK Corpus](https://datashare.ed.ac.uk/handle/10283/3443)

**Recording tips:**
- Use a decent microphone (phone mic is okay)
- Record in a quiet environment
- Speak naturally in Hindi or English
- Minimum 10 seconds, maximum 60 seconds per sample
- Mix of male and female voices recommended

### AI-Generated Voice Samples

**Recommended sources:**
1. **ElevenLabs** (https://elevenlabs.io/)
   - Free tier available
   - High-quality voice synthesis
   
2. **Murf.ai** (https://murf.ai/)
   - Multiple voices available
   - Good for testing
   
3. **Play.ht** (https://play.ht/)
   - Natural-sounding AI voices
   
4. **Google Cloud TTS** or **Azure TTS**
   - API-based generation
   - Various voices and languages

**Generation tips:**
- Generate same text in multiple AI voices
- Mix male and female AI voices
- Include both Hindi and English samples
- Save as MP3 or WAV format

## Minimum Requirements

For training a basic model:
- **Human samples**: At least 20 files
- **AI samples**: At least 20 files

For good performance:
- **Human samples**: 50+ files
- **AI samples**: 50+ files

For production-ready model:
- **Human samples**: 100+ files
- **AI samples**: 100+ files
- Diverse speakers, ages, accents
- Various recording conditions

## Supported Formats

- MP3
- WAV
- FLAC
- OGG
- M4A

## Privacy & Ethics

⚠️ **Important:**
- Only use audio you have permission to use
- Do not include private/sensitive recordings
- Follow local privacy laws
- If using public datasets, check their licenses

## Quick Start

```bash
# Create sample structure
mkdir -p data/human data/ai

# Add your files
cp /path/to/human/recordings/*.mp3 data/human/
cp /path/to/ai/samples/*.mp3 data/ai/

# Train model
python train.py
```

## Need Sample Data?

For hackathon testing, you can:

1. **Quick test dataset** (10 mins):
   - Record 10 voice memos on your phone → data/human/
   - Generate 10 samples with ElevenLabs → data/ai/

2. **Better dataset** (1 hour):
   - Download 50 samples from Common Voice → data/human/
   - Generate 50 samples with multiple AI services → data/ai/

3. **Production dataset** (ongoing):
   - Collect diverse real-world recordings
   - Include edge cases (noisy, accented, etc.)
   - Balance classes carefully

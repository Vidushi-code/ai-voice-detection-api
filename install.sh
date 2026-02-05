#!/bin/bash

# ============================================================
# AI VOICE DETECTION SYSTEM - INSTALLATION SCRIPT (Linux/Mac)
# ============================================================
# 
# This script will set up the complete environment
# Run with: bash install.sh
#
# ============================================================

echo ""
echo "============================================================"
echo "AI VOICE DETECTION SYSTEM - INSTALLATION"
echo "============================================================"
echo ""

# Check Python
echo "[1/6] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3.8+ first."
    exit 1
fi
python3 --version
echo ""

# Create virtual environment
echo "[2/6] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "[3/6] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "[4/6] Installing dependencies (this may take 2-3 minutes)..."
python -m pip install --upgrade pip setuptools wheel
echo "Installing core build tools..."
pip install setuptools wheel
echo "Installing project dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"
echo ""

# Create data directories
echo "[5/6] Creating data directories..."
mkdir -p data/human
mkdir -p data/ai
echo "✓ Data directories created"
echo ""

# Check data
echo "[6/6] Checking training data..."
human_count=$(ls -1 data/human/ 2>/dev/null | wc -l)
ai_count=$(ls -1 data/ai/ 2>/dev/null | wc -l)

echo "  Human voice samples: $human_count"
echo "  AI-generated samples: $ai_count"
echo ""

if [ $human_count -lt 10 ]; then
    echo "⚠️  WARNING: Less than 10 human samples found"
    echo "   Please add audio files to data/human/"
fi

if [ $ai_count -lt 10 ]; then
    echo "⚠️  WARNING: Less than 10 AI samples found"
    echo "   Please add audio files to data/ai/"
fi
echo ""

# Summary
echo "============================================================"
echo "INSTALLATION COMPLETE!"
echo "============================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Add training data:"
echo "   - Place human voice recordings in: data/human/"
echo "   - Place AI-generated samples in: data/ai/"
echo "   - Minimum: 20 samples per class"
echo "   - Recommended: 50+ samples per class"
echo ""
echo "2. Train the model:"
echo "   python train.py"
echo ""
echo "3. Start the API:"
echo "   python main.py"
echo ""
echo "4. Test it:"
echo "   Open http://localhost:8000/docs in your browser"
echo ""
echo "============================================================"
echo "For detailed instructions, see:"
echo "- QUICKSTART.md (5-minute guide)"
echo "- README.md (full documentation)"
echo "- 00_START_HERE.txt (complete overview)"
echo "============================================================"
echo ""

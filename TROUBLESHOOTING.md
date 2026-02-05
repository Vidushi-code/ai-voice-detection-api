# Troubleshooting Guide

## Common Installation Issues

### Issue 1: "Cannot import 'setuptools.build_meta'"

**Error:**
```
pip._vendor.pyproject_hooks._impl.BackendUnavailable: Cannot import 'setuptools.build_meta'
```

**Solution:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate

# Install build tools FIRST
python -m pip install --upgrade pip setuptools wheel

# Then install requirements
pip install -r requirements.txt
```

**Why this happens:**
New virtual environments on Windows sometimes don't include setuptools by default. Many packages need setuptools to build.

---

### Issue 2: "No module named 'numpy'" or "No module named 'fastapi'"

**Error:**
```
ModuleNotFoundError: No module named 'numpy'
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
# Activate virtual environment
venv\Scripts\activate

# Verify you're in the virtual environment (should show venv path)
where python

# Install all dependencies
pip install -r requirements.txt
```

**Why this happens:**
Dependencies weren't installed successfully. Always activate the virtual environment before installing packages.

---

### Issue 3: Virtual Environment Not Activating

**Windows PowerShell Error:**
```
cannot be loaded because running scripts is disabled
```

**Solution:**
```powershell
# Run PowerShell as Administrator, then:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again:
venv\Scripts\activate
```

**Alternative (Command Prompt):**
```cmd
# Use Command Prompt instead of PowerShell
venv\Scripts\activate.bat
```

---

### Issue 4: Installation Taking Too Long

**Solution:**
```bash
# Use a specific mirror (faster in some regions)
pip install -r requirements.txt --index-url https://pypi.org/simple
```

---

### Issue 5: "Microsoft Visual C++ 14.0 or greater is required"

**Solution:**
Install Microsoft C++ Build Tools:
1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install "Desktop development with C++"
3. Restart terminal and try again

**Or use pre-built wheels:**
```bash
pip install --only-binary :all: -r requirements.txt
```

---

### Issue 6: Librosa Installation Fails

**Error:**
```
ERROR: Failed building wheel for librosa
```

**Solution:**
```bash
# Install audio dependencies first
pip install soundfile audioread scipy numpy

# Then install librosa
pip install librosa
```

**Windows specific:**
```bash
# Install ffmpeg for audio processing
# Download from: https://ffmpeg.org/download.html
# Or use chocolatey:
choco install ffmpeg
```

---

## Verification Commands

### Check Python Version
```bash
python --version
# Should show Python 3.8 or higher
```

### Check Virtual Environment
```bash
# Windows
where python
# Should show: ...\ai-impact\venv\Scripts\python.exe

# Linux/Mac
which python
# Should show: .../ai-impact/venv/bin/python
```

### Check Installed Packages
```bash
pip list
# Should show numpy, scikit-learn, fastapi, etc.
```

### Test Imports
```bash
python -c "import numpy; print('numpy OK')"
python -c "import sklearn; print('sklearn OK')"
python -c "import librosa; print('librosa OK')"
python -c "import fastapi; print('fastapi OK')"
```

---

## Clean Reinstall

If all else fails, start fresh:

```bash
# 1. Delete virtual environment
rmdir /s venv  # Windows
rm -rf venv    # Linux/Mac

# 2. Create new virtual environment
python -m venv venv

# 3. Activate it
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 4. Install build tools FIRST
python -m pip install --upgrade pip setuptools wheel

# 5. Install dependencies
pip install -r requirements.txt
```

---

## Quick Fix Script (Windows)

Save as `fix_install.bat`:

```batch
@echo off
echo Fixing installation...

echo Step 1: Activating virtual environment...
call venv\Scripts\activate.bat

echo Step 2: Upgrading pip and build tools...
python -m pip install --upgrade pip setuptools wheel

echo Step 3: Installing dependencies...
pip install -r requirements.txt

echo Done! Try running: python main.py
pause
```

Run with: `fix_install.bat`

---

## Quick Fix Script (Linux/Mac)

Save as `fix_install.sh`:

```bash
#!/bin/bash
echo "Fixing installation..."

echo "Step 1: Activating virtual environment..."
source venv/bin/activate

echo "Step 2: Upgrading pip and build tools..."
python -m pip install --upgrade pip setuptools wheel

echo "Step 3: Installing dependencies..."
pip install -r requirements.txt

echo "Done! Try running: python main.py"
```

Run with: `bash fix_install.sh`

---

## Still Having Issues?

### Option 1: Use System Python (Not Recommended)
```bash
# Install globally (skip virtual environment)
pip install -r requirements.txt
python main.py
```

### Option 2: Use Conda Instead
```bash
conda create -n ai-impact python=3.10
conda activate ai-impact
pip install -r requirements.txt
```

### Option 3: Use Docker
```bash
docker build -t ai-voice .
docker run -p 8000:8000 ai-voice
```

---

## Platform-Specific Notes

### Windows 11
- Use PowerShell or Command Prompt (not Git Bash)
- May need to run as Administrator for first-time setup
- Antivirus may slow down installation

### macOS
- May need Xcode Command Line Tools: `xcode-select --install`
- On Apple Silicon (M1/M2), some packages may need Rosetta

### Linux
- May need system packages: `sudo apt install python3-dev build-essential`
- For audio: `sudo apt install libsndfile1 ffmpeg`

---

## Success Checklist

✅ Python 3.8+ installed  
✅ Virtual environment created and activated  
✅ pip, setuptools, wheel upgraded  
✅ All requirements.txt packages installed  
✅ Can import numpy, sklearn, librosa, fastapi  
✅ No errors when running `python --version`  

Once all checked, you're ready to:
```bash
python train.py   # Train model
python main.py    # Start API
```

---

## Need More Help?

1. Check [README.md](README.md) for detailed setup
2. See [QUICKSTART.md](QUICKSTART.md) for step-by-step guide
3. Review error messages carefully - they often contain the solution

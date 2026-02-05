:: ============================================================
:: AI VOICE DETECTION SYSTEM - INSTALLATION SCRIPT (Windows)
:: ============================================================
:: 
:: This script will set up the complete environment
:: Run this in Command Prompt or PowerShell
::
:: ============================================================

@echo off
echo.
echo ============================================================
echo AI VOICE DETECTION SYSTEM - INSTALLATION
echo ============================================================
echo.

:: Check Python
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.8+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

:: Create virtual environment
echo [2/6] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv venv
    echo ✓ Virtual environment created
)
echo.

:: Activate virtual environment
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

:: Install dependencies
echo [4/6] Installing dependencies (this may take 2-3 minutes)...
python -m pip install --upgrade pip setuptools wheel
echo Installing core build tools...
pip install setuptools wheel
echo Installing project dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

:: Create data directories
echo [5/6] Creating data directories...
if not exist "data\human" mkdir "data\human"
if not exist "data\ai" mkdir "data\ai"
echo ✓ Data directories created
echo.

:: Check data
echo [6/6] Checking training data...
set human_count=0
set ai_count=0
for %%f in (data\human\*.*) do set /a human_count+=1
for %%f in (data\ai\*.*) do set /a ai_count+=1

echo   Human voice samples: %human_count%
echo   AI-generated samples: %ai_count%
echo.

if %human_count% lss 10 (
    echo ⚠️  WARNING: Less than 10 human samples found
    echo    Please add audio files to data\human\
)

if %ai_count% lss 10 (
    echo ⚠️  WARNING: Less than 10 AI samples found
    echo    Please add audio files to data\ai\
)
echo.

:: Summary
echo ============================================================
echo INSTALLATION COMPLETE!
echo ============================================================
echo.
echo Next steps:
echo.
echo 1. Add training data:
echo    - Place human voice recordings in: data\human\
echo    - Place AI-generated samples in: data\ai\
echo    - Minimum: 20 samples per class
echo    - Recommended: 50+ samples per class
echo.
echo 2. Train the model:
echo    python train.py
echo.
echo 3. Start the API:
echo    python main.py
echo.
echo 4. Test it:
echo    Open http://localhost:8000/docs in your browser
echo.
echo ============================================================
echo For detailed instructions, see:
echo - QUICKSTART.md (5-minute guide)
echo - README.md (full documentation)
echo - 00_START_HERE.txt (complete overview)
echo ============================================================
echo.

pause

@echo off
echo 📚 Book Summarizer AI - Windows Startup
echo ======================================

echo.
echo 🔧 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found

echo.
echo 📦 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed

echo.
echo 🚀 Starting Book Summarizer AI...
python start.py

pause 
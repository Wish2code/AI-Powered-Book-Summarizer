@echo off
echo Book Summarizer - Windows Startup
echo ================================

python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    pause
    exit /b 1
)

echo Installing dependencies (if needed)...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo Launching Streamlit...
python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0

pause

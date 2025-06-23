#!/usr/bin/env python3
"""
Startup script for Book Summarizer AI
This script helps you start both the FastAPI backend and Streamlit frontend.
"""

import subprocess
import sys
import time
import requests
import os
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        'streamlit', 'fastapi', 'uvicorn', 'transformers', 
        'torch', 'PyPDF2', 'pdfplumber', 'nltk'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install them with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def download_nltk_data():
    """Download required NLTK data."""
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✅ NLTK data downloaded")
    except Exception as e:
        print(f"⚠️  Warning: Could not download NLTK data: {e}")

def check_api_health():
    """Check if the API is running and healthy."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_api():
    """Start the FastAPI backend."""
    print("🚀 Starting FastAPI backend...")
    
    # Check if API is already running
    if check_api_health():
        print("✅ API is already running")
        return True
    
    try:
        # Start the API server
        api_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "api.main:app", 
            "--reload", 
            "--port", "8000",
            "--host", "0.0.0.0"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for API to start
        print("⏳ Waiting for API to start...")
        for i in range(30):  # Wait up to 30 seconds
            time.sleep(1)
            if check_api_health():
                print("✅ API started successfully")
                return True
        
        print("❌ API failed to start within 30 seconds")
        return False
        
    except Exception as e:
        print(f"❌ Error starting API: {e}")
        return False

def start_frontend():
    """Start the Streamlit frontend."""
    print("🌐 Starting Streamlit frontend...")
    
    try:
        # Start Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")

def main():
    """Main startup function."""
    print("📚 Book Summarizer AI - Startup")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Download NLTK data
    download_nltk_data()
    
    print("\n🔧 Starting services...")
    
    # Start API
    if not start_api():
        print("❌ Failed to start API. Please check the logs.")
        sys.exit(1)
    
    print("\n🎉 Ready! Opening the application...")
    print("📖 Frontend: http://localhost:8501")
    print("🔌 API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\n💡 Press Ctrl+C to stop the application")
    
    # Start frontend
    start_frontend()

if __name__ == "__main__":
    main() 
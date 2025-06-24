#!/usr/bin/env python3
"""
Deployment Helper Script for Book Summarizer AI
This script validates your project structure and provides deployment guidance.
"""

import os
import sys
from pathlib import Path

def check_project_structure():
    """Check if all required files are present for deployment."""
    print("🔍 Checking project structure...")
    
    required_files = [
        "app.py",
        "requirements.txt",
        "Procfile",
        "runtime.txt",
        "api/main.py",
        "api/summarizer.py",
        "api/pdf_processor.py",
        "api/utils.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required files present")
        return True

def check_environment_variables():
    """Check if environment variables are properly configured."""
    print("\n🔧 Checking environment configuration...")
    
    # Check if app.py uses environment variables
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            content = f.read()
            if "os.getenv" in content:
                print("✅ app.py configured to use environment variables")
            else:
                print("❌ app.py needs to be updated to use environment variables")
    except Exception as e:
        print(f"⚠️ Could not check app.py configuration: {e}")
        print("   Please manually verify that app.py uses os.getenv for API_BASE_URL")

def show_deployment_steps():
    """Display deployment steps."""
    print("\n🚀 DEPLOYMENT STEPS:")
    print("=" * 50)
    
    print("\n1️⃣ BACKEND DEPLOYMENT (Railway):")
    print("   • Go to https://railway.app")
    print("   • Sign up with GitHub")
    print("   • Create new project from GitHub repo")
    print("   • Add environment variable: PORT=8000")
    print("   • Get your backend URL")
    
    print("\n2️⃣ FRONTEND DEPLOYMENT (Streamlit Cloud):")
    print("   • Go to https://share.streamlit.io")
    print("   • Sign in with GitHub")
    print("   • Create new app")
    print("   • Repository: Your GitHub repo")
    print("   • Main file path: app.py")
    print("   • Add environment variable: API_BASE_URL=your-railway-url")
    
    print("\n3️⃣ TESTING:")
    print("   • Test backend: your-railway-url/docs")
    print("   • Test frontend: your-streamlit-url")
    print("   • Upload a PDF and generate summary")

def main():
    """Main deployment helper function."""
    print("📚 Book Summarizer AI - Deployment Helper")
    print("=" * 50)
    
    # Check project structure
    if not check_project_structure():
        print("\n❌ Please fix missing files before deploying")
        sys.exit(1)
    
    # Check environment configuration
    check_environment_variables()
    
    # Show deployment steps
    show_deployment_steps()
    
    print("\n📖 For detailed instructions, see DEPLOYMENT.md")
    print("🎉 Ready to deploy!")

if __name__ == "__main__":
    main() 
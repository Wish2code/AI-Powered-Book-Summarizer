#!/bin/bash

echo "📚 Book Summarizer AI - Unix/Linux/Mac Startup"
echo "=============================================="

echo ""
echo "🔧 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

echo "✅ Python 3 found"

echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"

echo ""
echo "🚀 Starting Book Summarizer AI..."
python3 start.py 
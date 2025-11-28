#!/bin/bash

echo "Book Summarizer - Startup"
echo "========================="

if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in PATH."
    exit 1
fi

echo "Installing dependencies (if needed)..."
pip3 install -r requirements.txt || {
    echo "Failed to install dependencies."
    exit 1
}

echo "Launching Streamlit..."
python3 -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0

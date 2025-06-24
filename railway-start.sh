#!/bin/bash

# Download NLTK data
echo "📥 Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Start the FastAPI server
echo "🚀 Starting Book Summarizer API..."
uvicorn api.main:app --host 0.0.0.0 --port $PORT 
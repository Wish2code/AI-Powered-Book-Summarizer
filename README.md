# 📚 Book Summarizer AI

An intelligent web application that extracts text from PDF books and generates comprehensive summaries using state-of-the-art AI models.

## ✨ Features

- 📚 **PDF Text Extraction**: Advanced PDF processing with multiple extraction methods
- 🤖 **AI-Powered Summarization**: Uses transformer models (BART, T5) for high-quality summaries
- 🌐 **Beautiful Web Interface**: Modern UI built with Streamlit
- ⚡ **FastAPI Backend**: Scalable and fast API for processing
- 📝 **Configurable Settings**: Adjust summary length, chunk size, and AI models
- 📊 **Text Analysis**: Detailed statistics about book content
- 💾 **Download Summaries**: Save summaries as text files

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
# Double-click start.bat or run:
start.bat
```

**Unix/Linux/Mac:**
```bash
# Make script executable and run:
chmod +x start.sh
./start.sh
```

### Option 2: Manual Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Download NLTK data:**
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

3. **Start the FastAPI backend:**
```bash
uvicorn api.main:app --reload --port 8000
```

4. **Start the Streamlit frontend:**
```bash
streamlit run app.py
```

5. **Open your browser:**
   - Frontend: http://localhost:8501
   - API Docs: http://localhost:8000/docs

## 📖 Usage

1. **Upload PDF**: Select a PDF book file (max 50MB)
2. **Configure Settings**: Choose AI model and summary parameters
3. **Generate Summary**: Click "Generate Summary" and wait for processing
4. **Download Result**: Save your AI-generated summary

## 🛠️ Technology Stack

### Frontend
- **Streamlit**: Modern web interface
- **Custom CSS**: Beautiful styling and responsive design

### Backend
- **FastAPI**: High-performance API framework
- **Uvicorn**: ASGI server for FastAPI

### AI & ML
- **Hugging Face Transformers**: State-of-the-art NLP models
- **PyTorch**: Deep learning framework
- **BART/T5 Models**: Pre-trained summarization models

### PDF Processing
- **PyPDF2**: PDF text extraction
- **pdfplumber**: Advanced PDF processing
- **NLTK**: Natural language processing

## 📁 Project Structure

```
book-summarizer/
├── app.py                 # Streamlit frontend
├── start.py              # Automated startup script
├── start.bat             # Windows startup script
├── start.sh              # Unix/Linux/Mac startup script
├── api/
│   ├── __init__.py       # API package
│   ├── main.py           # FastAPI backend
│   ├── pdf_processor.py  # PDF text extraction
│   ├── summarizer.py     # AI summarization logic
│   └── utils.py          # Utility functions
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## ⚙️ Configuration

### AI Models
- **facebook/bart-large-cnn**: Best quality, slower processing
- **t5-small**: Faster processing, good quality
- **facebook/bart-base**: Balanced performance

### Summary Settings
- **Max Length**: 50-500 words (default: 150)
- **Min Length**: 10-200 words (default: 50)
- **Chunk Size**: 500-2000 characters (default: 1000)
- **Overlap**: 50-200 characters (default: 100)

## 🔧 API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /upload-pdf` - Validate PDF file
- `POST /extract-text` - Extract text from PDF
- `POST /summarize` - Generate book summary
- `GET /models` - List available AI models
- `POST /change-model` - Switch AI model

## 📋 Requirements

- **Python**: 3.8 or higher
- **Memory**: At least 4GB RAM (8GB recommended)
- **Storage**: 2GB free space for models
- **Internet**: Required for first-time model download

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" errors:**
   ```bash
   pip install -r requirements.txt
   ```

2. **NLTK data missing:**
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

3. **API connection failed:**
   - Ensure FastAPI is running on port 8000
   - Check firewall settings
   - Verify no other service is using the port

4. **Large PDF processing slow:**
   - Reduce chunk size in advanced settings
   - Use a faster model (t5-small)
   - Ensure sufficient RAM

5. **Model download issues:**
   - Check internet connection
   - Clear Hugging Face cache: `rm -rf ~/.cache/huggingface`

### Performance Tips

- **GPU Acceleration**: Install CUDA for faster processing
- **Model Selection**: Use smaller models for faster results
- **Chunk Size**: Smaller chunks = faster processing but may lose context
- **Memory**: Close other applications to free up RAM

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Hugging Face for transformer models
- Streamlit for the web framework
- FastAPI for the backend framework
- The open-source community for various libraries

## 📞 Support

For issues, questions, or feature requests:
1. Check the troubleshooting section
2. Open an issue on GitHub

---

**Happy summarizing! 📚✨** 

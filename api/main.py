from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
import asyncio
from .pdf_processor import PDFProcessor
from .summarizer import BookSummarizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Book Summarizer API",
    description="AI-powered book summarization service",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
pdf_processor = PDFProcessor()
summarizer = BookSummarizer()

# Pydantic models
class SummaryRequest(BaseModel):
    max_length: int = 150
    min_length: int = 50
    chunk_size: int = 1000
    overlap: int = 100
    model_name: Optional[str] = None

class SummaryResponse(BaseModel):
    success: bool
    summary: str
    statistics: Dict[str, Any]
    message: str

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup."""
    logger.info("Starting Book Summarizer API...")
    try:
        # Load the summarization model
        summarizer.load_model()
        logger.info("API startup completed successfully")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Book Summarizer API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": summarizer.summarizer is not None
    }

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and validate a PDF file.
    """
    try:
        # Check file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Read file content
        content = await file.read()
        
        # Validate PDF
        validation_result = pdf_processor.validate_pdf(content)
        if not validation_result['valid']:
            raise HTTPException(status_code=400, detail=validation_result['message'])
        
        # Extract metadata
        metadata = pdf_processor.get_pdf_metadata(content)
        
        return {
            "success": True,
            "filename": file.filename,
            "size_mb": validation_result['size_mb'],
            "pages": validation_result['pages'],
            "metadata": metadata,
            "message": "PDF uploaded and validated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    """
    Extract text from uploaded PDF.
    """
    try:
        # Read file content
        content = await file.read()
        
        # Extract text
        result = pdf_processor.extract_text_from_pdf(content)
        
        if not result['success']:
            raise HTTPException(status_code=400, detail=result['message'])
        
        return {
            "success": True,
            "text_length": len(result['text']),
            "statistics": result['statistics'],
            "pages": result['pages'],
            "message": result['message']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error extracting text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")

@app.post("/summarize")
async def summarize_book(
    file: UploadFile = File(...),
    request: SummaryRequest = SummaryRequest()
):
    """
    Summarize a book from uploaded PDF.
    """
    try:
        # Read file content
        content = await file.read()
        
        # Extract text
        extraction_result = pdf_processor.extract_text_from_pdf(content)
        if not extraction_result['success']:
            raise HTTPException(status_code=400, detail=extraction_result['message'])
        
        # Change model if specified
        if request.model_name:
            summarizer.change_model(request.model_name)
        
        # Summarize the book
        summary_result = summarizer.summarize_book(
            text=extraction_result['text'],
            chunk_size=request.chunk_size,
            overlap=request.overlap,
            max_length=request.max_length,
            min_length=request.min_length
        )
        
        if not summary_result['success']:
            raise HTTPException(status_code=500, detail=summary_result.get('error', 'Summarization failed'))
        
        return {
            "success": True,
            "summary": summary_result['summary'],
            "statistics": summary_result['statistics'],
            "original_statistics": extraction_result['statistics'],
            "message": "Book summarized successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error summarizing book: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error summarizing book: {str(e)}")

@app.get("/models")
async def get_available_models():
    """
    Get list of available summarization models.
    """
    try:
        models = summarizer.get_available_models()
        return {
            "success": True,
            "models": models,
            "current_model": summarizer.model_name
        }
    except Exception as e:
        logger.error(f"Error getting models: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting models: {str(e)}")

@app.post("/change-model")
async def change_model(model_name: str):
    """
    Change the summarization model.
    """
    try:
        summarizer.change_model(model_name)
        summarizer.load_model()
        
        return {
            "success": True,
            "message": f"Model changed to {model_name}",
            "current_model": model_name
        }
    except Exception as e:
        logger.error(f"Error changing model: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error changing model: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Get port from environment variable (for Railway deployment)
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 
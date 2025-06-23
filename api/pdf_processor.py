import PyPDF2
import pdfplumber
import io
from typing import Dict, Any, Optional
import logging
from .utils import clean_text, get_text_statistics

logger = logging.getLogger(__name__)

class PDFProcessor:
    """
    Handles PDF text extraction and processing.
    """
    
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def extract_text_from_pdf(self, pdf_file: bytes) -> Dict[str, Any]:
        """
        Extract text from PDF file bytes.
        
        Args:
            pdf_file: PDF file as bytes
            
        Returns:
            Dictionary containing extracted text and metadata
        """
        try:
            # Try pdfplumber first (better for complex layouts)
            text = self._extract_with_pdfplumber(pdf_file)
            
            if not text or len(text.strip()) < 100:
                # Fallback to PyPDF2
                text = self._extract_with_pypdf2(pdf_file)
            
            if not text:
                raise ValueError("Could not extract text from PDF")
            
            # Clean the extracted text
            cleaned_text = clean_text(text)
            
            # Get text statistics
            stats = get_text_statistics(cleaned_text)
            
            return {
                'success': True,
                'text': cleaned_text,
                'statistics': stats,
                'pages': self._get_page_count(pdf_file),
                'message': 'Text extracted successfully'
            }
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            return {
                'success': False,
                'text': '',
                'statistics': {},
                'pages': 0,
                'message': f'Error extracting text: {str(e)}'
            }
    
    def _extract_with_pdfplumber(self, pdf_file: bytes) -> str:
        """
        Extract text using pdfplumber (better for complex layouts).
        """
        text_parts = []
        
        try:
            with pdfplumber.open(io.BytesIO(pdf_file)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
            
            return '\n'.join(text_parts)
        except Exception as e:
            logger.warning(f"pdfplumber extraction failed: {str(e)}")
            return ""
    
    def _extract_with_pypdf2(self, pdf_file: bytes) -> str:
        """
        Extract text using PyPDF2 (fallback method).
        """
        text_parts = []
        
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
            
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            
            return '\n'.join(text_parts)
        except Exception as e:
            logger.warning(f"PyPDF2 extraction failed: {str(e)}")
            return ""
    
    def _get_page_count(self, pdf_file: bytes) -> int:
        """
        Get the number of pages in the PDF.
        """
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
            return len(pdf_reader.pages)
        except:
            return 0
    
    def get_pdf_metadata(self, pdf_file: bytes) -> Dict[str, Any]:
        """
        Extract metadata from PDF file.
        """
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
            metadata = pdf_reader.metadata
            
            return {
                'title': metadata.get('/Title', 'Unknown'),
                'author': metadata.get('/Author', 'Unknown'),
                'subject': metadata.get('/Subject', ''),
                'creator': metadata.get('/Creator', ''),
                'producer': metadata.get('/Producer', ''),
                'pages': len(pdf_reader.pages)
            }
        except Exception as e:
            logger.error(f"Error extracting PDF metadata: {str(e)}")
            return {
                'title': 'Unknown',
                'author': 'Unknown',
                'subject': '',
                'creator': '',
                'producer': '',
                'pages': 0
            }
    
    def validate_pdf(self, pdf_file: bytes) -> Dict[str, Any]:
        """
        Validate PDF file and check if it can be processed.
        """
        try:
            # Check file size
            file_size = len(pdf_file)
            max_size = 50 * 1024 * 1024  # 50MB limit
            
            if file_size > max_size:
                return {
                    'valid': False,
                    'message': f'File too large. Maximum size is 50MB, got {file_size / (1024*1024):.1f}MB'
                }
            
            # Try to read PDF
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
            
            if len(pdf_reader.pages) == 0:
                return {
                    'valid': False,
                    'message': 'PDF appears to be empty or corrupted'
                }
            
            return {
                'valid': True,
                'message': 'PDF is valid',
                'pages': len(pdf_reader.pages),
                'size_mb': file_size / (1024 * 1024)
            }
            
        except Exception as e:
            return {
                'valid': False,
                'message': f'Invalid PDF file: {str(e)}'
            } 
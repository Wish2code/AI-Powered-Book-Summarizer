from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from typing import List, Dict, Any, Optional, Union
import torch
import logging
from .utils import chunk_text

logger = logging.getLogger(__name__)

class BookSummarizer:
    """
    Handles AI-powered text summarization using transformer models.
    """
    
    def __init__(self, model_name: str = "sshleifer/distilbart-cnn-6-6"):
        """
        Initialize the summarizer with a specific model.
        
        Args:
            model_name: Hugging Face model name for summarization
        """
        self.model_name = model_name
        self.summarizer = None
        self.tokenizer = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        logger.info(f"Initializing summarizer with model: {model_name}")
        logger.info(f"Using device: {self.device}")
    
    def load_model(self):
        """
        Load the summarization model and tokenizer.
        """
        try:
            logger.info("Loading summarization model...")
            
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            
            # Move model to appropriate device
            self.model.to(self.device)
            
            # Create pipeline
            self.summarizer = pipeline(
                "summarization",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1
            )
            
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def summarize_text(self, text: str, max_length: int = 150, min_length: int = 50, 
                      do_sample: bool = False) -> Dict[str, Any]:
        """
        Summarize a single text chunk.
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            do_sample: Whether to use sampling for generation
            
        Returns:
            Dictionary containing summary and metadata
        """
        try:
            if not self.summarizer:
                self.load_model()
            
            # Check if text is too short
            if len(text.split()) < 50:
                return {
                    'success': True,
                    'summary': text,
                    'original_length': len(text.split()),
                    'summary_length': len(text.split()),
                    'compression_ratio': 1.0
                }
            
            # Generate summary
            summary_result = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=do_sample,
                truncation=True
            )
            
            summary = summary_result[0]['summary_text']
            
            # Calculate compression ratio
            original_words = len(text.split())
            summary_words = len(summary.split())
            compression_ratio = summary_words / original_words if original_words > 0 else 0
            
            return {
                'success': True,
                'summary': summary,
                'original_length': original_words,
                'summary_length': summary_words,
                'compression_ratio': compression_ratio
            }
            
        except Exception as e:
            logger.error(f"Error summarizing text: {str(e)}")
            return {
                'success': False,
                'summary': '',
                'error': str(e)
            }
    
    def summarize_book(self, text: str, chunk_size: int = 1000, overlap: int = 100,
                      max_length: int = 150, min_length: int = 50) -> Dict[str, Any]:
        """
        Summarize a complete book by processing it in chunks.
        
        Args:
            text: Complete book text
            chunk_size: Size of each text chunk
            overlap: Overlap between chunks
            max_length: Maximum length of each summary
            min_length: Minimum length of each summary
            
        Returns:
            Dictionary containing complete summary and metadata
        """
        try:
            logger.info("Starting book summarization...")
            
            # Split text into chunks
            chunks = chunk_text(text, chunk_size, overlap)
            logger.info(f"Split text into {len(chunks)} chunks")
            
            # Summarize each chunk
            chunk_summaries = []
            total_original_words = 0
            total_summary_words = 0
            
            for i, chunk in enumerate(chunks):
                logger.info(f"Processing chunk {i+1}/{len(chunks)}")
                
                result = self.summarize_text(chunk, max_length, min_length)
                
                if result['success']:
                    chunk_summaries.append(result['summary'])
                    total_original_words += result['original_length']
                    total_summary_words += result['summary_length']
                else:
                    logger.warning(f"Failed to summarize chunk {i+1}: {result.get('error', 'Unknown error')}")
                    # Include original chunk if summarization fails
                    chunk_summaries.append(chunk[:200] + "...")
            
            # Combine all summaries
            combined_summary = " ".join(chunk_summaries)
            
            # Create final summary if the combined summary is still too long
            if len(combined_summary.split()) > 500:
                logger.info("Creating final summary from combined summaries...")
                final_result = self.summarize_text(combined_summary, max_length=300, min_length=100)
                if final_result['success']:
                    combined_summary = final_result['summary']
            
            # Calculate overall statistics
            overall_compression = total_summary_words / total_original_words if total_original_words > 0 else 0
            
            return {
                'success': True,
                'summary': combined_summary,
                'statistics': {
                    'total_chunks': len(chunks),
                    'total_original_words': total_original_words,
                    'total_summary_words': total_summary_words,
                    'overall_compression_ratio': overall_compression,
                    'final_summary_length': len(combined_summary.split())
                },
                'chunk_summaries': chunk_summaries
            }
            
        except Exception as e:
            logger.error(f"Error in book summarization: {str(e)}")
            return {
                'success': False,
                'summary': '',
                'error': str(e)
            }
    
    def get_available_models(self) -> List[Dict[str, Union[str, int]]]:
        """
        Get list of available summarization models.
        """
        return [
            {
                'name': 'facebook/bart-large-cnn',
                'description': 'BART model fine-tuned on CNN news articles (recommended)',
                'max_length': 1024
            },
            {
                'name': 't5-small',
                'description': 'Small T5 model, faster but less accurate',
                'max_length': 512
            },
            {
                'name': 'facebook/bart-base',
                'description': 'Base BART model, balanced performance',
                'max_length': 1024
            }
        ]
    
    def change_model(self, model_name: str):
        """
        Change the summarization model.
        
        Args:
            model_name: New model name to use
        """
        self.model_name = model_name
        self.summarizer = None
        self.tokenizer = None
        self.model = None
        logger.info(f"Model changed to: {model_name}") 
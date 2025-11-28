import re
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """
    Clean and preprocess extracted text from PDF.
    """
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    text = text.strip()
    
    # Remove common PDF artifacts
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}]', '', text)
    
    return text

def chunk_text(text: str, max_chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """
    Split text into overlapping chunks for processing.
    
    Args:
        text: Input text to chunk
        max_chunk_size: Maximum size of each chunk
        overlap: Number of characters to overlap between chunks
    
    Returns:
        List of text chunks
    """
    if len(text) <= max_chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + max_chunk_size
        
        # Try to break at sentence boundaries
        if end < len(text):
            # Look for sentence endings
            sentence_endings = ['.', '!', '?']
            for ending in sentence_endings:
                last_ending = text.rfind(ending, start, end)
                if last_ending > start + max_chunk_size * 0.8:  # Only break if we're at least 80% through
                    end = last_ending + 1
                    break
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move start position with overlap
        start = end - overlap
        if start >= len(text):
            break
    
    return chunks

def extract_chapters(text: str) -> Dict[str, str]:
    """
    Attempt to extract chapters from the text.
    """
    chapters = {}
    
    # Common chapter patterns
    chapter_patterns = [
        r'Chapter\s+(\d+|[IVXLC]+)',
        r'CHAPTER\s+(\d+|[IVXLC]+)',
        r'(\d+)\.\s+[A-Z]',
        r'[IVXLC]+\.\s+[A-Z]'
    ]
    
    lines = text.split('\n')
    current_chapter = "Introduction"
    current_content = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this line is a chapter header
        is_chapter_header = False
        for pattern in chapter_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                # Save previous chapter
                if current_content:
                    chapters[current_chapter] = '\n'.join(current_content)
                
                current_chapter = line
                current_content = []
                is_chapter_header = True
                break
        
        if not is_chapter_header:
            current_content.append(line)
    
    # Save the last chapter
    if current_content:
        chapters[current_chapter] = '\n'.join(current_content)
    
    return chapters

def get_text_statistics(text: str) -> Dict[str, Any]:
    """
    Get basic statistics about the text.
    """
    words = text.split()
    # Lightweight sentence split to avoid NLTK downloads
    sentences = [s.strip() for s in re.split(r'(?<=[\.\!\?])\s+', text) if s.strip()]
    
    return {
        'total_characters': len(text),
        'total_words': len(words),
        'total_sentences': len(sentences),
        'average_words_per_sentence': len(words) / len(sentences) if sentences else 0,
        'estimated_reading_time_minutes': len(words) / 200  # Average reading speed
    }

import streamlit as st
import requests
import json
import time
from typing import Dict, Any, Optional
import io
import os

# Page configuration
st.set_page_config(
    page_title="Book Summarizer AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API configuration - use environment variable for deployment
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def main():
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">📚 Book Summarizer AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform your PDF books into intelligent summaries using AI</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Model selection
        st.subheader("AI Model")
        try:
            models_response = requests.get(f"{API_BASE_URL}/models")
            if models_response.status_code == 200:
                models_data = models_response.json()
                models = models_data.get('models', [])
                current_model = models_data.get('current_model', '')
                
                model_names = [model['name'] for model in models]
                selected_model = st.selectbox(
                    "Choose AI Model",
                    model_names,
                    index=model_names.index(current_model) if current_model in model_names else 0
                )
                
                # Show model description
                selected_model_info = next((m for m in models if m['name'] == selected_model), None)
                if selected_model_info:
                    st.info(f"**{selected_model_info['description']}**")
            else:
                st.error("Failed to load models")
                selected_model = "facebook/bart-large-cnn"
        except Exception as e:
            st.error(f"Error loading models: {str(e)}")
            selected_model = "facebook/bart-large-cnn"
        
        # Summary settings
        st.subheader("Summary Settings")
        max_length = st.slider("Maximum Summary Length", 50, 500, 150, help="Maximum number of words in the summary")
        min_length = st.slider("Minimum Summary Length", 10, 200, 50, help="Minimum number of words in the summary")
        
        # Advanced settings
        with st.expander("Advanced Settings"):
            chunk_size = st.slider("Chunk Size", 500, 2000, 1000, help="Size of text chunks for processing")
            overlap = st.slider("Chunk Overlap", 50, 200, 100, help="Overlap between text chunks")
        
        # API status
        st.subheader("API Status")
        try:
            health_response = requests.get(f"{API_BASE_URL}/health")
            if health_response.status_code == 200:
                st.success("✅ API Connected")
            else:
                st.error("❌ API Error")
        except:
            st.error("❌ API Unavailable")
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📖 Summarize Book", "📊 Text Analysis", "ℹ️ About"])
    
    with tab1:
        st.header("📖 Book Summarization")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a PDF book file",
            type=['pdf'],
            help="Upload a PDF file (max 50MB)"
        )
        
        if uploaded_file is not None:
            # File info
            file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # MB
            st.info(f"📄 **File:** {uploaded_file.name} ({file_size:.1f} MB)")
            
            # Validate file
            if st.button("🔍 Validate PDF", type="secondary"):
                with st.spinner("Validating PDF..."):
                    try:
                        files = {"file": uploaded_file.getvalue()}
                        response = requests.post(f"{API_BASE_URL}/upload-pdf", files=files)
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.success(f"✅ {data['message']}")
                            
                            # Display metadata
                            metadata = data.get('metadata', {})
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Pages", data['pages'])
                            with col2:
                                st.metric("Size", f"{data['size_mb']:.1f} MB")
                            with col3:
                                st.metric("Title", metadata.get('title', 'Unknown'))
                        else:
                            st.error(f"❌ Validation failed: {response.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            
            # Summarize button
            if st.button("🚀 Generate Summary", type="primary"):
                if uploaded_file is not None:
                    with st.spinner("Processing your book..."):
                        try:
                            # Prepare request
                            files = {"file": uploaded_file.getvalue()}
                            data = {
                                "max_length": max_length,
                                "min_length": min_length,
                                "chunk_size": chunk_size,
                                "overlap": overlap,
                                "model_name": selected_model
                            }
                            
                            # Send request
                            response = requests.post(f"{API_BASE_URL}/summarize", files=files, data=data)
                            
                            if response.status_code == 200:
                                result = response.json()
                                
                                # Display success message
                                st.success("✅ Summary generated successfully!")
                                
                                # Display statistics
                                col1, col2, col3, col4 = st.columns(4)
                                stats = result.get('statistics', {})
                                orig_stats = result.get('original_statistics', {})
                                
                                with col1:
                                    st.metric("Original Words", f"{orig_stats.get('total_words', 0):,}")
                                with col2:
                                    st.metric("Summary Words", f"{stats.get('final_summary_length', 0):,}")
                                with col3:
                                    compression = stats.get('overall_compression_ratio', 0)
                                    st.metric("Compression", f"{compression:.1%}")
                                with col4:
                                    st.metric("Chunks Processed", stats.get('total_chunks', 0))
                                
                                # Display summary
                                st.subheader("📝 Generated Summary")
                                summary = result.get('summary', '')
                                st.text_area(
                                    "Summary",
                                    value=summary,
                                    height=400,
                                    disabled=True
                                )
                                
                                # Download button
                                summary_bytes = summary.encode('utf-8')
                                st.download_button(
                                    label="📥 Download Summary",
                                    data=summary_bytes,
                                    file_name=f"{uploaded_file.name.replace('.pdf', '')}_summary.txt",
                                    mime="text/plain"
                                )
                                
                            else:
                                error_msg = response.json().get('detail', 'Unknown error')
                                st.error(f"❌ Summarization failed: {error_msg}")
                                
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
    
    with tab2:
        st.header("📊 Text Analysis")
        
        if uploaded_file is not None:
            if st.button("📊 Analyze Text"):
                with st.spinner("Analyzing text..."):
                    try:
                        files = {"file": uploaded_file.getvalue()}
                        response = requests.post(f"{API_BASE_URL}/extract-text", files=files)
                        
                        if response.status_code == 200:
                            data = response.json()
                            stats = data.get('statistics', {})
                            
                            # Display statistics
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric("Total Words", f"{stats.get('total_words', 0):,}")
                            with col2:
                                st.metric("Total Sentences", f"{stats.get('total_sentences', 0):,}")
                            with col3:
                                st.metric("Avg Words/Sentence", f"{stats.get('average_words_per_sentence', 0):.1f}")
                            with col4:
                                st.metric("Reading Time", f"{stats.get('estimated_reading_time_minutes', 0):.1f} min")
                            
                            # Text preview
                            st.subheader("📄 Text Preview")
                            text_response = requests.post(f"{API_BASE_URL}/extract-text", files=files)
                            if text_response.status_code == 200:
                                text_data = text_response.json()
                                preview_text = text_data.get('text', '')[:1000] + "..." if len(text_data.get('text', '')) > 1000 else text_data.get('text', '')
                                st.text_area("First 1000 characters:", value=preview_text, height=200, disabled=True)
                        else:
                            st.error(f"❌ Analysis failed: {response.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        else:
            st.info("📄 Please upload a PDF file to analyze its text.")
    
    with tab3:
        st.header("ℹ️ About")
        
        st.markdown("""
        ## 🤖 Book Summarizer AI
        
        This application uses advanced AI models to automatically summarize PDF books. 
        It processes the text in chunks and generates comprehensive summaries while 
        maintaining the key information and context.
        
        ### ✨ Features
        
        - **PDF Text Extraction**: Advanced PDF processing with fallback methods
        - **AI Summarization**: State-of-the-art transformer models
        - **Configurable Settings**: Adjust summary length and processing parameters
        - **Multiple Models**: Choose from different AI models for various use cases
        - **Text Analysis**: Detailed statistics about the book content
        
        ### 🛠️ Technology Stack
        
        - **Frontend**: Streamlit
        - **Backend**: FastAPI
        - **AI Models**: Hugging Face Transformers (BART, T5)
        - **PDF Processing**: PyPDF2, pdfplumber
        - **Text Processing**: NLTK
        
        ### 📋 How It Works
        
        1. **Upload**: Select a PDF book file (max 50MB)
        2. **Extract**: The system extracts and cleans text from the PDF
        3. **Chunk**: Large texts are split into manageable chunks
        4. **Summarize**: AI models process each chunk and generate summaries
        5. **Combine**: Individual summaries are combined into a final summary
        6. **Download**: Get your summary in text format
        
        ### 🚀 Getting Started
        
        1. Make sure the API server is running (`uvicorn api.main:app --reload`)
        2. Upload a PDF book file
        3. Configure your preferred settings
        4. Click "Generate Summary" and wait for processing
        5. Download your AI-generated summary
        
        ### 📞 Support
        
        For issues or questions, please check the API documentation at `/docs` 
        when the server is running.
        """)

if __name__ == "__main__":
    main() 
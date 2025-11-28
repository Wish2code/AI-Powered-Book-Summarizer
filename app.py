import os
import streamlit as st
from typing import Dict, Any

from api.pdf_processor import PDFProcessor
from api.summarizer import BookSummarizer

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "sshleifer/distilbart-cnn-12-6")
AVAILABLE_MODELS = BookSummarizer(DEFAULT_MODEL).get_available_models()


st.set_page_config(
    page_title="Book Summarizer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def get_pdf_processor() -> PDFProcessor:
    return PDFProcessor()


@st.cache_resource
def get_summarizer(model_name: str) -> BookSummarizer:
    summarizer = BookSummarizer(model_name=model_name)
    summarizer.load_model()
    return summarizer


def summarize_pdf(
    uploaded_file,
    model_name: str,
    max_length: int,
    min_length: int,
    chunk_size: int,
    overlap: int,
) -> Dict[str, Any]:
    pdf_bytes = uploaded_file.getvalue()
    processor = get_pdf_processor()

    validation = processor.validate_pdf(pdf_bytes)
    if not validation["valid"]:
        raise ValueError(validation["message"])

    metadata = processor.get_pdf_metadata(pdf_bytes)
    extraction = processor.extract_text_from_pdf(pdf_bytes)
    if not extraction["success"]:
        raise RuntimeError(extraction["message"])

    summarizer = get_summarizer(model_name)
    summary_result = summarizer.summarize_book(
        text=extraction["text"],
        chunk_size=chunk_size,
        overlap=overlap,
        max_length=max_length,
        min_length=min_length,
    )

    if not summary_result["success"]:
        raise RuntimeError(summary_result.get("error", "Summarization failed"))

    return {
        "metadata": metadata,
        "validation": validation,
        "extraction": extraction,
        "summary": summary_result,
    }


def sidebar_controls():
    st.header("Settings")

    model_names = [m["name"] for m in AVAILABLE_MODELS]
    model_descriptions = {m["name"]: m["description"] for m in AVAILABLE_MODELS}

    selected_model = st.selectbox(
        "Model",
        model_names,
        index=model_names.index(DEFAULT_MODEL) if DEFAULT_MODEL in model_names else 0,
        help="Free, locally run Hugging Face models. First run downloads weights.",
    )
    st.caption(model_descriptions.get(selected_model, ""))

    max_length = st.slider(
        "Maximum summary length (words)",
        min_value=50,
        max_value=250,
        value=140,
        step=10,
    )
    min_length = st.slider(
        "Minimum summary length (words)",
        min_value=20,
        max_value=min_length_limit := min(120, max_length - 10),
        value=min(50, max_length - 20),
        step=5,
    )

    chunk_size = st.slider(
        "Chunk size (characters)",
        min_value=600,
        max_value=2000,
        value=1200,
        step=50,
        help="Longer chunks preserve context but take longer.",
    )
    overlap = st.slider(
        "Chunk overlap (characters)",
        min_value=50,
        max_value=300,
        value=120,
        step=10,
    )

    return {
        "model": selected_model,
        "max_length": max_length,
        "min_length": min_length,
        "chunk_size": chunk_size,
        "overlap": overlap,
    }


def show_file_info(uploaded_file):
    size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
    st.info(f"Selected: **{uploaded_file.name}** ({size_mb:.1f} MB)")


def show_results(result: Dict[str, Any]):
    summary_text = result["summary"]["summary"]
    stats = result["summary"]["statistics"]
    original_stats = result["extraction"]["statistics"]

    st.success("Summary ready!")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pages", result["validation"]["pages"])
    col2.metric("Original words", f"{original_stats.get('total_words', 0):,}")
    col3.metric("Summary words", f"{stats.get('final_summary_length', 0):,}")
    compression = stats.get("overall_compression_ratio", 0)
    col4.metric("Compression", f"{compression:.1%}" if compression else "N/A")

    st.subheader("Summary")
    st.text_area("Generated summary", value=summary_text, height=400, label_visibility="collapsed")

    st.download_button(
        label="Download summary",
        data=summary_text.encode("utf-8"),
        file_name=f"{result['metadata'].get('title', 'summary').replace(' ', '_')}.txt",
        mime="text/plain",
    )

    st.subheader("Book snapshot")
    preview = result["extraction"]["text"][:1500]
    if len(result["extraction"]["text"]) > 1500:
        preview += " ..."
    st.text_area("First 1500 characters", value=preview, height=220, label_visibility="collapsed")


def main():
    st.title("📚 AI-Powered Book Summarizer")
    st.write(
        "Upload a PDF (under 50MB) to generate a concise summary locally with free, open models. "
        "No paid API keys required—first run will download model weights."
    )

    st.divider()

    with st.sidebar:
        controls = sidebar_controls()

    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file:
        show_file_info(uploaded_file)
        if st.button("Generate summary", type="primary"):
            with st.spinner("Extracting text and generating summary..."):
                try:
                    result = summarize_pdf(
                        uploaded_file=uploaded_file,
                        model_name=controls["model"],
                        max_length=controls["max_length"],
                        min_length=controls["min_length"],
                        chunk_size=controls["chunk_size"],
                        overlap=controls["overlap"],
                    )
                    show_results(result)
                except Exception as exc:
                    st.error(f"Could not summarize this PDF: {exc}")
    else:
        st.info("Upload a small/medium PDF to get started. Scans or image-only PDFs will not work well.")


if __name__ == "__main__":
    main()

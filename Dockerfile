FROM python:3.10-slim

# System deps for PDF parsing
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    poppler-utils \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first for better cache hits
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Default model can be overridden in Space settings
ENV DEFAULT_MODEL=t5-small
ENV PORT=7860

EXPOSE 7860

# Start Streamlit on the expected port/interface
CMD ["streamlit", "run", "app.py", "--server.port", "7860", "--server.address", "0.0.0.0"]

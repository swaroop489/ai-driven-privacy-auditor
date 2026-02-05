FROM python:3.10-slim

WORKDIR /app

# Install runtime dependencies for Tesseract
# --no-install-recommends keeps it small (no docs, extra langs)
# tesseract-ocr-eng ensures English support is present
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 8000

# Command to run (mapped to 8002 in compose)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

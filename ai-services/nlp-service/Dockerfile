FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model explicitly
RUN python -m spacy download en_core_web_sm

# Copy app code
COPY . .

# Expose port
EXPOSE 8000

# Command to run
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
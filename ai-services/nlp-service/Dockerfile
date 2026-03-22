FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Note: Model is installed via requirements.txt, so manual download step is removed

# Copy app code
COPY . .

# Ensure the custom model is explicitly copied
COPY model /app/model

# Expose port
EXPOSE 8000

# Command to run
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
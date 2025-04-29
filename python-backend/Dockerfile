# Use slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy app files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5001

# Start Flask app
CMD ["python", "model_api.py"]

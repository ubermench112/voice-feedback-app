FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (ffmpeg required for audio)
RUN apt-get update \
    && apt-get install -y ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list first (Docker cache optimization)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Flask port
EXPOSE 3000

# Run Flask app
CMD ["python", "app.py"]

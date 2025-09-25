# Use Python 3.11 (more stable with camelot-py than 3.12)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for camelot-py
RUN apt-get update && apt-get install -y \
    ghostscript \
    libgs-dev \
    libpoppler-cpp-dev \
    pkg-config \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libopenjp2-7-dev \
    libwebp-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev \
    libgtk-3-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libatlas-base-dev \
    gfortran \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY web-ui/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app/src:/app/web-ui
ENV FLASK_APP=web-ui/app.py

# Expose port
EXPOSE 8080

# Run the application
CMD ["cd", "web-ui", "&&", "python", "app.py"]

# Use Python 3.11 with Ubuntu base (more stable for system packages)
FROM python:3.11-slim-bullseye

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
    gfortran \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install ghostscript Python bindings
RUN pip install --no-cache-dir ghostscript

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
EXPOSE 5000

# Run the application
CMD ["python", "web-ui/app.py"]

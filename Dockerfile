# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required by Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libglib2.0-0 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libcairo2 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libxrandr2 \
    libxss1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY api/requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (this will persist in the Docker image)
RUN playwright install chromium

# Copy application code
COPY api /app/api

# Set working directory to api
WORKDIR /app/api

# Expose port
EXPOSE 8080

# Start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

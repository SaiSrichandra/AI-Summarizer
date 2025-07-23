FROM python:3.11-slim

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies for Chrome
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    curl \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libgbm1 \
    chromium \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver
ENV PATH="${PATH}:/usr/bin/chromium"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app
WORKDIR /app

# Run FastAPI app
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
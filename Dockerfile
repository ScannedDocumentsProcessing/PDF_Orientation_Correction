# Base image
FROM python:3.11

# Install all required packages to run the model
# TODO: 1. Add any additional packages required to run your model
# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
# RUN pip3 install opencv-python-headless==4.11.0.86
RUN apt update && \
    apt install -y tesseract-ocr libtesseract-dev && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Work directory
WORKDIR /app

# Copy requirements file
COPY ./requirements.txt .
COPY ./requirements-all.txt .

# Install dependencies
RUN pip install --requirement requirements.txt --requirement requirements-all.txt

# Copy sources
COPY src src

# Environment variables
ENV ENVIRONMENT=${ENVIRONMENT}
ENV LOG_LEVEL=${LOG_LEVEL}
ENV ENGINE_URL=${ENGINE_URL}
ENV MAX_TASKS=${MAX_TASKS}
ENV ENGINE_ANNOUNCE_RETRIES=${ENGINE_ANNOUNCE_RETRIES}
ENV ENGINE_ANNOUNCE_RETRY_DELAY=${ENGINE_ANNOUNCE_RETRY_DELAY}

# Exposed ports
EXPOSE 80

# Switch to src directory
WORKDIR "/app/src"

# Command to run on start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

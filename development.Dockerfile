# Base image
FROM python:3.11

# Install all required packages to run the model
# TODO: 1. Add any additional packages required to run your model
# RUN apt update && apt install --yes package1 package2 ...
RUN apt update && \
    apt install -y tesseract-ocr libtesseract-dev && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Copy sources
COPY src src
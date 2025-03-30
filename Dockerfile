# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /oura_pipeline

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    curl \
    ca-certificates \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml
COPY pyproject.toml .
COPY requirements.txt .

# Install just the dependencies without trying to install the package itself
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["/bin/bash"]
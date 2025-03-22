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
    && rm -rf /var/lib/apt/lists/*

# Download the latest uv installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the PATH
ENV PATH="/root/.local/bin/:$PATH"

# Copy pyproject.toml
COPY pyproject.toml .

# Install just the dependencies without trying to install the package itself
RUN uv pip install --system dlt[duckdb]==1.8.1 sqlmesh==0.167.1

# Create .dlt directory for secrets if it doesn't exist
RUN mkdir -p /oura_pipeline/.dlt

# Use bash as the entrypoint
ENTRYPOINT ["/bin/bash"]
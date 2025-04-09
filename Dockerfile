# Use an official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app
ENV PYTHONPATH=/app

# Install build tools
RUN apt-get update && apt-get install -y curl gcc libffi-dev && rm -rf /var/lib/apt/lists/*

# Copy the whole project into the image
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install .

# Entrypoint
COPY docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
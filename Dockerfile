# Use an official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install pipenv or use pip + build tools
RUN apt-get update && apt-get install -y curl gcc libffi-dev && rm -rf /var/lib/apt/lists/*

# Copy and install project dependencies
COPY pyproject.toml ./
COPY content_request ./content_request
COPY prompts ./prompts
COPY output ./output
COPY logs ./logs

RUN pip install --upgrade pip build && \
    pip install .

# Copy entrypoint script (if you have one, e.g. quickstart)
COPY docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Default to showing help
ENTRYPOINT ["contentgen"]
CMD ["--help"]
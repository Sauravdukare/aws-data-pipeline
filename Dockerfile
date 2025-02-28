# Use Python 3.9 as the base image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependencies first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt -t /app/deps

# Copy all application files
COPY . .

# Set the Python path
ENV PYTHONPATH="/app/deps"

# Run the correct script
CMD ["python", "/app/app.py"]

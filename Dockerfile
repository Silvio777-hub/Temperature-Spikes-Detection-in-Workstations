# Use slim python image for efficiency
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for building some wheels if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Ensure logs and models directories exist
RUN mkdir -p logs models reports

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run (defaults to simulation mode since hardware access is restricted in generic Docker)
ENTRYPOINT ["python", "monitor.py"]
CMD ["simulate"]

# Start with the official Python slim image for a smaller container
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Install build essentials (gcc, etc.) AND PostgreSQL client libraries (libpq-dev)
# libpq-dev is CRITICAL for successfully installing psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
# Note: You MUST ensure 'psycopg2-binary' is in your requirements.txt now.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the application startup command using the robust Exec Form
# This structure is correct for Railway and assumes $PORT is set in the environment.
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT", "--workers", "1", "--log-level", "info"]

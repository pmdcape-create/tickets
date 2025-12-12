# Start with the official Python slim image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Install build essentials (gcc) needed for some Python packages and clean up
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# *** FIX APPLIED HERE ***
# Use the JSON array form for CMD with 'sh -c' to ensure
# shell variable expansion (${PORT:-8080}) works correctly.
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-8080} --workers 1 --log-level info"]

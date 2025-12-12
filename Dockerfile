# Start with the official Python slim image for a smaller container
FROM python:3.13-slim

# Set the working directory inside the container (Should be done early)
WORKDIR /app

# Install build essentials and CRITICAL PostgreSQL client libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# *** TEMPORARY LINE TO BREAK CACHE AND FORCE NEW INSTALL ***
RUN echo "Triggering fresh build"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the application startup command using the robust Exec Form.
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT", "--workers", "1", "--log-level", "info"]

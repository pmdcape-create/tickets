# Start with the official Python slim image for a smaller container
FROM python:3.13-slim

# Set the working directory inside the container (Should be done early)
WORKDIR /app

# Install build essentials and CRITICAL PostgreSQL client libraries
# libpq-dev is necessary for psycopg2 to compile correctly.
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# *** TEMPORARY LINE TO BREAK CACHE AND FORCE NEW INSTALL ***
# This forces Docker to re-run all steps below it, ensuring psycopg2 is installed.
RUN echo "Triggering fresh build"

# Copy requirements and install dependencies
# Note: Ensure 'psycopg2-binary' is in your requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the application startup command using the robust Exec Form.
# This reliably passes the $PORT variable to Gunicorn.
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT", "--workers", "1", "--log-level", "info"]

# Start with the official Python slim image for a smaller container
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Install build essentials (gcc) needed for some Python packages and clean up
# This ensures that packages with C extensions (like psycopg2) can be installed
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
# This is done separately to leverage Docker's build cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# *** THE FINAL FIX: Exec Form Array (No Shell) ***
# This avoids using 'sh -c' entirely and directly executes gunicorn,
# passing $PORT as an argument. This is the most reliable structure.
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT", "--workers", "1", "--log-level", "info"]

# Use lightweight official Python image
FROM python:3.13-slim

# Set working directory inside container
WORKDIR /app

# Install gcc (needed for some Python packages like reportlab/psycopg2)
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Tell the container which port Railway will give us
ENV PORT=8080

# Start the app with Gunicorn
CMD gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --log-level info

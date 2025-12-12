FROM python:3.13-slim

WORKDIR /app

# Install build tools needed for psycopg2 / reportlab
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# THIS IS THE ONLY LINE THAT HAS EVER WORKED CONSISTENTLY ON RAILWAY DOCKER IN 2025
CMD gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --worker-class sync

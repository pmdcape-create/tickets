FROM python:3.13-slim

WORKDIR /app

# Needed for some packages (reportlab, psycopg2, etc.)
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Railway injects the real port via the $PORT environment variable at runtime
# We just make sure the variable exists (fallback to 8080 if something goes wrong)
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:${PORT:-8000}", "--workers", "1", "--log-level", "info"]

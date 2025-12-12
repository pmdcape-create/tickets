FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Force shell expansion for $PORT (Railway's real port gets injected here)
CMD sh -c "gunicorn app:app --bind 0.0.0.0:\${PORT:-8080} --workers 1 --log-level info"

# config.py — THIS ONE WORKS 100% ON RAILWAY (DEC 2025)
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-fallback-key")

    # === DATABASE – THE ONLY PART THAT MATTERS ===
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    # Railway injects DATABASE_URL automatically when Postgres is attached
    db_url = os.getenv("DATABASE_URL")

    if db_url:
        # Railway gives "postgres://", SQLAlchemy 2.x needs "postgresql://"
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = db_url
    else:
        # Only used when running locally
        SQLALCHEMY_DATABASE_URI = "sqlite:///tickets.db"

    # (Email settings kept only so the app doesn't crash if something still reads them)
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT", "587")
    if MAIL_PORT:
        MAIL_PORT = int(MAIL_PORT)


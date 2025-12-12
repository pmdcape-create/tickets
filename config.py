# config.py — FINAL SAFE VERSION (works on Railway + local)
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-for-local-dev")

    # ───── Email (only kept for compatibility — we now use Resend) ─────
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT", 587)
    if MAIL_PORT is not None:
        MAIL_PORT = int(MAIL_PORT)
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_TIMEOUT = 20

    # Where tickets get forwarded (optional — we hard-coded in utils.py for now)
    TICKET_DESTINATION_EMAILS = {
        "Maintenance": os.getenv("DEST_MAINTENANCE", "pmdcape@gmail.com"),
        "Information":  os.getenv("DEST_INFO", "pmdcape@gmail.com"),
        "Finance":      os.getenv("DEST_FINANCE", "pmdcape@gmail.com"),
        "General":      os.getenv("DEST_GENERAL", "pmdcape@gmail.com"),
    }

    # ───── Database Configuration (Railway + Local) ─────
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Fix Railway's postgres:// → postgresql://
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or "sqlite:///tickets.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False





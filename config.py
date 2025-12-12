# config.py — SAFE VERSION
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-for-local-dev")

    # Email — everything comes from Railway variables
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", MAIL_USERNAME)
    MAIL_TIMEOUT = 20

    # Where tickets get forwarded
    TICKET_DESTINATION_EMAILS = {
        "Maintenance": os.getenv("DEST_MAINTENANCE", "pmdcape@gmail.com"),
        "Information":  os.getenv("DEST_INFO", "pmdcape@gmail.com"),
        "Finance":      os.getenv("DEST_FINANCE", "pmdcape@gmail.com"),
        "General":      os.getenv("DEST_GENERAL", "pmdcape@gmail.com"),
    }

    # ───── Database Configuration (Railway + Local) ─────
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Railway gives "postgres://" but SQLAlchemy wants "postgresql://"
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or "sqlite:///tickets.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    )
    




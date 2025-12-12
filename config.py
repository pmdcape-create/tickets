# config.py — 100% WORKING FINAL VERSION
import os
from urllib.parse import urlparse

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # Email settings (we use Resend now – these are just for compatibility)
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT", "587")
    if MAIL_PORT:
        MAIL_PORT = int(MAIL_PORT)
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    # DATABASE – THE ONLY PART THAT MATTERS
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Default fallback for local development
    SQLALCHEMY_DATABASE_URI = "sqlite:///tickets.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # If Railway gave us a DATABASE_URL → use it (and fix postgres→postgresql)
    if DATABASE_URL:
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL

    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}





# File: config.py

import os

class Config:
    SECRET_KEY = "your-secret-key"

    # Email settings
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # ADD THIS LINE TO PREVENT TIMEOUTS
    MAIL_TIMEOUT = 30
    MAIL_USERNAME = "janvanderwalt2025@gmail.com"
    MAIL_PASSWORD = "gwdalnypihqizbhf"  # WARNING: Consider using Railway Environment Variables for secrets
    MAIL_DEFAULT_SENDER = "janvanderwalt2025@gmail.com"

    # Ticket destination emails
    TICKET_DESTINATION_EMAILS = {
        "Maintenance": "pmdcape@gmail.com",
        "Information": "pmdcape@gmail.com",
        "Finance": "pmdcape@gmail.com",
        "General": "pmdcape@gmail.com",
    }

    # Database (CRITICAL FIX: Changed from absolute Windows path to a relative path)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tickets.db' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False


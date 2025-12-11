# File: config.py

import os

class Config:
    # --- Secrets and Basic Configuration ---
    SECRET_KEY = "your-secret-key"

    # --- Email Settings (FIXED FOR RAILWAY DEPLOYMENT) ---
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465       # <-- CRITICAL CHANGE: Use secure port 465
    MAIL_USE_TLS = False  # <-- CRITICAL CHANGE: Disable TLS
    MAIL_USE_SSL = True   # <-- ADDED: Enable SSL protocol for port 465
    MAIL_TIMEOUT = 30     # High timeout kept as a safeguard
    
    MAIL_USERNAME = "janvanderwalt2025@gmail.com"
    MAIL_PASSWORD = "gwdalnypihqizbhf" # WARNING: Highly recommend moving this to a Railway Environment Variable!
    MAIL_DEFAULT_SENDER = "janvanderwalt2025@gmail.com"

    # --- Ticket Destination Emails ---
    TICKET_DESTINATION_EMAILS = {
        "Maintenance": "pmdcape@gmail.com",
        "Information": "pmdcape@gmail.com",
        "Finance": "pmdcape@gmail.com",
        "General": "pmdcape@gmail.com",
    }

    # --- Database Configuration ---
    # Uses a relative path so the SQLite file is created inside the container
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tickets.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False



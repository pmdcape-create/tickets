# config.py
import os

class Config:
    SECRET_KEY = "your-secret-key"

    # Email settings...
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "janvanderwalt2025@gmail.com"
    MAIL_PASSWORD = "gwdalnypihqizbhf"
    MAIL_DEFAULT_SENDER = "janvanderwalt2025@gmail.com"

    # Ticket destination emails...
    TICKET_DESTINATION_EMAILS = {
        "Maintenance": "pmdcape@gmail.com",
        "Information": "pmdcape@gmail.com",
        "Finance": "pmdcape@gmail.com",
        "General": "pmdcape@gmail.com",
    }

    # Database (absolute path)
    SQLALCHEMY_DATABASE_URI = r"sqlite:///C:/Users/Janvdw/Documents/tickets_db/tickets.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

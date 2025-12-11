import os
from app import app
from extensions import db
from models import Ticket

# Absolute path to the clean folder
DB_FILE = r"C:\Users\Janvdw\Documents\tickets_db\tickets.db"
print("Trying to create database at:", DB_FILE)

# Ensure folder exists
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

try:
    # Remove old database if it exists
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"{DB_FILE} removed.")

    # Create new database and tables
    with app.app_context():
        db.create_all()
        print("Database and tables created successfully!")

    # Check if DB file now exists
    print("DB file exists after creation?", os.path.exists(DB_FILE))

except Exception as e:
    print("Error while creating DB:", e)

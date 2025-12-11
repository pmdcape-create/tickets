# create_db_debug2.py
import os
from app import app
from extensions import db
from models import Ticket

DB_FILE = r"C:\temp\tickets.db"
print("Trying to create database at:", DB_FILE)

try:
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"{DB_FILE} removed.")

    with app.app_context():
        db.create_all()
        print("Database and tables created successfully!")

    print("DB file exists after creation?", os.path.exists(DB_FILE))

except Exception as e:
    print("Error while creating DB:", e)


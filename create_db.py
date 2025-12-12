import os
from app import app
from extensions import db
from models import Ticket

# --- Logic to handle database initialization based on environment ---

# Check if the PostgreSQL connection URI is set (meaning we are running remotely on Railway)
if os.environ.get('SQLALCHEMY_DATABASE_URI'):
    print("Remote environment detected. Using SQLALCHEMY_DATABASE_URI for PostgreSQL.")
    
    # In a remote environment, we only need to run db.create_all()
    # No need to manage local files or directories.
    try:
        with app.app_context():
            db.create_all()
            print("PostgreSQL tables created successfully!")
            
    except Exception as e:
        print("Error while creating PostgreSQL DB tables:", e)

else:
    # --- This block runs ONLY if SQLALCHEMY_DATABASE_URI is NOT set (e.g., local development) ---
    DB_FILE = "tickets_db/tickets.db" # Using a relative path for safer local use
    print("Local environment detected. Using SQLite:", DB_FILE)
    
    # Ensure local folder exists
    try:
        os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
        
        # Configure app to use the local SQLite file (Ensure this is also in app.py for local run)
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_FILE}'
        
        # Remove old database if it exists
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            print(f"{DB_FILE} removed.")
        
        # Create new database and tables
        with app.app_context():
            db.create_all()
            print("SQLite tables created successfully!")
            print("DB file exists after creation?", os.path.exists(DB_FILE))
            
    except Exception as e:
        print("Error while creating local SQLite DB:", e)

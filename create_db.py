import os
from app import app
from extensions import db
from models import Ticket

# Check for EITHER the standard Flask-SQLAlchemy var OR the common Railway var.
# This ensures the script correctly detects the PostgreSQL environment during the Pre-Deploy step.
is_remote = os.environ.get('SQLALCHEMY_DATABASE_URI') or os.environ.get('DATABASE_URL')

if is_remote:
    # --- This block runs on Railway (PostgreSQL) ---
    print("Remote environment detected. Using PostgreSQL.")
    
    # In a remote environment, we only need to run db.create_all()
    try:
        with app.app_context():
            # Crucial: Ensure the app configuration prioritizes the ENV variable
            # This is usually done in app.py, but re-checking here for safety.
            
            # If the app's config is not already set by one of the ENV variables, 
            # we must set it explicitly here before calling db.create_all().
            
            # Note: Assuming your app.py is correctly configured to read these variables.
            db.create_all() 
            print("PostgreSQL tables created successfully!")
            
    except Exception as e:
        print("Error while creating PostgreSQL DB tables:", e)
        # Re-raise the exception to show the failure in the logs and stop the deployment
        # This is better than silently failing.
        raise

else:
    # --- This block runs ONLY if no remote URI is found (e.g., local development) ---
    DB_FILE = "tickets_db/tickets.db" 
    print("Local environment detected. Using SQLite:", DB_FILE)
    
    # Ensure local folder exists
    try:
        # Note: You need to ensure the app.config['SQLALCHEMY_DATABASE_URI'] 
        # is set to the SQLite path in app.py for this to work locally.
        os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
        
        # Configure app to use the local SQLite file (Necessary for db.create_all() here)
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
        # Stop the local execution
        raise


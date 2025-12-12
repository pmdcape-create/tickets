# File: app.py

import os
from flask import Flask
from datetime import datetime # <-- MUST BE AT THE TOP
from extensions import db, mail
from config import Config
from routes.ticket_routes import ticket_bp
from routes.admin_routes import admin_bp
# 🚨 ADD THIS IMPORT 🚨
from flask_migrate import Migrate 

# -----------------------------------------------------------------
# CRITICAL: Use the Factory Pattern (create_app) for Railway/Gunicorn
# -----------------------------------------------------------------
def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    # Set DEBUG mode explicitly, often good practice during development
    app.config['DEBUG'] = True
    
    # Initialize extensions with the app
    db.init_app(app)
    mail.init_app(app)

    # 🚨 INITIALIZE FLASK-MIGRATE HERE 🚨
    # This links the Flask app instance and the SQLAlchemy instance (db)
    # so the 'flask db' commands know what to track.
    migrate = Migrate(app, db) # ⬅️ Assign the Migrate object to a variable
    
    # FIX: Register 'now()' as a global function for templates
    # This must be done AFTER the 'app' object is created.
    app.jinja_env.globals.update(now=datetime.now)
    
    # Register Blueprints
    app.register_blueprint(ticket_bp)
    app.register_blueprint(admin_bp)

    # IMPORTANT: Ensure the database is created within the app context
    # NOTE: db.create_all() is fine for the first run, but rely on 
    # migrations (flask db upgrade) for all subsequent schema changes.
    with app.app_context():
        db.create_all()

    return app

# -----------------------------------------------------------------
# Entry points for production (Gunicorn) and local development
# -----------------------------------------------------------------

# Gunicorn/Production entry point (Used by Railway)
# Flask-Migrate needs this 'app' instance to be available.
app = create_app()

# Only used when running locally with python app.py
if __name__ == '__main__':
    # When running locally, use the app instance created by create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


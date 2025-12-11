# File: app.py

import os
from flask import Flask
# Import your extensions and configuration objects
from extensions import db, mail
from config import Config
# Import your blueprints to link your application routes
from routes.ticket_routes import ticket_bp
from routes.admin_routes import admin_bp

# Initialize Flask app
app = Flask(__name__)
# Load configuration from your config.py file
app.config.from_object(Config)

# Initialize extensions with the app
db.init_app(app)
mail.init_app(app)

# Register Blueprints - THIS LOADS YOUR REAL TICKET AND ADMIN PAGES
app.register_blueprint(ticket_bp)
app.register_blueprint(admin_bp)

# -----------------------------------------------------------------
# CRITICAL FIX: Correctly initialize the database at Gunicorn startup
# This replaces the deprecated @app.before_first_request decorator
with app.app_context():
    db.create_all()
# -----------------------------------------------------------------

# Only used when running locally with python app.py
if __name__ == '__main__':
    # Use 0.0.0.0:$PORT for Railway production, 5000 for local dev
    # Note: Gunicorn will handle this in production, but this is safe for local testing
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))



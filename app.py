import os
from flask import Flask
from extensions import db, mail
from config import Config
from routes.ticket_routes import ticket_bp
from routes.admin_routes import admin_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions with the app
db.init_app(app)
mail.init_app(app)

# Register Blueprints
app.register_blueprint(ticket_bp)
app.register_blueprint(admin_bp)

# Create database tables on the first request (works perfectly on Railway)
@app.before_first_request
def create_tables():
    db.create_all()

# Only used when running locally with python app.py
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

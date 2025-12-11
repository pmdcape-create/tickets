import os
from flask import Flask
from extensions import db, mail
from config import Config
from routes.ticket_routes import ticket_bp
from routes.admin_routes import admin_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
mail.init_app(app)

# Register Blueprints
app.register_blueprint(ticket_bp)
app.register_blueprint(admin_bp)

# Create database tables and run app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))



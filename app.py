from flask import Flask
from extensions import db, mail
from config import Config
from routes.ticket_routes import ticket_bp
from routes.admin_routes import admin_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
mail.init_app(app)

app.register_blueprint(ticket_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


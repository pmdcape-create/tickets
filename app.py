from flask import Flask
from extensions import db, mail

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'janvanderwalt2025@gmail.com'
app.config['MAIL_PASSWORD'] = 'gwdalnypihqizbhf'
app.config['MAIL_DEFAULT_SENDER'] = 'janvanderwalt2025@gmail.com'

# Initialize extensions
db.init_app(app)
mail.init_app(app)

# Example route
@app.route('/')
def home():
    return "Hello, Flask 3.x on Railway!"

# Initialize the database at startup
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

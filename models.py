# models.py
from extensions import db

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_no = db.Column(db.String(50), unique=True, nullable=False)
    scheme_name = db.Column(db.String(100), nullable=False)
    unit_no = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    contact_number = db.Column(db.String(50))
    email = db.Column(db.String(100))
    attachment = db.Column(db.String(200))  # new column
    status = db.Column(db.String(50), default="Pending")


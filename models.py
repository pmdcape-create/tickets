# models.py
# 1. Import datetime
from datetime import datetime 
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
    attachment = db.Column(db.String(200)) 
    status = db.Column(db.String(50), default="Pending")
    
    # 2. 🚨 CRITICAL ADDITION for Sorting and Auditing 🚨
    submitted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Ticket('{self.ticket_no}', '{self.status}')"



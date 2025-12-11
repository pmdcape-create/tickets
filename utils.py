from config import Config
from flask_mail import Message
from io import BytesIO
from reportlab.pdfgen import canvas
from flask import current_app

def send_ticket_email(ticket, mail):
    # Lookup the recipient from Config
    recipient = Config.TICKET_DESTINATION_EMAILS.get(ticket.category, Config.TICKET_DESTINATION_EMAILS["General"])

    msg = Message(
        subject=f"New Ticket: {ticket.ticket_no}",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[recipient],
        cc=[ticket.email]
    )

    msg.body = f"""
Ticket Number: {ticket.ticket_no}
Scheme Name: {ticket.scheme_name}
Unit No: {ticket.unit_no}
Category: {ticket.category}
Message: {ticket.message}
Contact: {ticket.contact_number}
Email: {ticket.email}
Status: {ticket.status}
"""

    # Attach the uploaded file if it exists
    if ticket.attachment:
        try:
            with open(ticket.attachment, "rb") as f:
                filename = ticket.attachment.split("/")[-1]
                msg.attach(filename, "application/octet-stream", f.read())
        except Exception as e:
            print(f"Failed to attach file: {e}")

    mail.send(msg)

def generate_ticket_pdf(ticket):
    pdf_buffer = BytesIO()
    p = canvas.Canvas(pdf_buffer)
    p.drawString(100, 800, f"Ticket Number: {ticket.ticket_no}")
    p.drawString(100, 780, f"Scheme Name: {ticket.scheme_name}")
    p.drawString(100, 760, f"Unit Number: {ticket.unit_no}")
    p.drawString(100, 740, f"Category: {ticket.category}")
    p.drawString(100, 720, f"Message: {ticket.message}")
    p.drawString(100, 700, f"Contact: {ticket.contact_number}")
    p.drawString(100, 680, f"Email: {ticket.email}")
    p.drawString(100, 660, f"Status: {ticket.status}")
    p.save()
    pdf_buffer.seek(0)
    return pdf_buffer

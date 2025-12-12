# utils.py
import os
from flask import current_app
from io import BytesIO
from reportlab.pdfgen import canvas

# Only try to import resend if we're using it (fails gracefully locally if not installed)
try:
    import resend
    resend.api_key = os.getenv("RESEND_API_KEY")
    RESEND_AVAILABLE = True
except Exception:
    RESEND_AVAILABLE = False


def send_ticket_email(ticket):
    """
    Sends notification email using Resend (production) 
    Falls back to nothing in local/dev if Resend not configured
    """
    if not RESEND_AVAILABLE or os.getenv("MAIL_PROVIDER") != "resend":
        print("Email sending skipped (Resend not configured or disabled)")
        return

    # Where the office/manager gets notified
    destination_email = "pmdcape@gmail.com"  # you can make this dynamic later

    # Nice HTML email for the tenant + manager
    html_body = f"""
    <h2>New Maintenance Ticket Received</h2>
    <p><strong>Ticket No:</strong> {ticket.ticket_no}</p>
    <p><strong>Scheme:</strong> {ticket.scheme_name}</p>
    <p><strong>Unit:</strong> {ticket.unit_no}</p>
    <p><strong>Category:</strong> {ticket.category}</p>
    <p><strong>Contact:</strong> {ticket.contact_number} | {ticket.email}</p>
    <p><strong>Message:</strong><br>{ticket.message.replace(chr(10), '<br>')}</p>
    <hr>
    <small>This is an automated notification from the PMDCape ticketing system.</small>
    """

    try:
        resend.Emails.send({
            "from": os.getenv("FROM_EMAIL", "pmdcape <onboarding@resend.dev>"),
            "to": [destination_email],
            "cc": [ticket.email],  # tenant gets a copy
            "subject": f"New Ticket #{ticket.ticket_no} – {ticket.category}",
            "html": html_body,
        })
        print(f"Email successfully sent via Resend for ticket {ticket.ticket_no}")
    except Exception as e:
        # --- FINAL CRASH TEST BLOCK ---
        # This will force the server to crash and log the exact error from Resend.
        print("-" * 50)
        print("!!! RESEND FAILED! CHECK THE TRACEBACK BELOW !!!")
        print(f"Error captured: {e}") 
        print("-" * 50)
        raise e # <--- FORCES CRASH AND LOGGING
        # --- END CRASH TEST BLOCK ---


def generate_ticket_pdf(ticket):
    """Returns PDF as BytesIO – unchanged and working perfectly"""
    pdf_buffer = BytesIO()
    p = canvas.Canvas(pdf_buffer)
    y = 800
    p.drawString(100, y, f"Ticket Number: {ticket.ticket_no}"); y -= 20
    p.drawString(100, y, f"Scheme Name: {ticket.scheme_name}"); y -= 20
    p.drawString(100, y, f"Unit Number: {ticket.unit_no}"); y -= 20
    p.drawString(100, y, f"Category: {ticket.category}"); y -= 20
    p.drawString(100, y, f"Message: {ticket.message}"); y -= 40
    p.drawString(100, y, f"Contact: {ticket.contact_number}"); y -= 20
    p.drawString(100, y, f"Email: {ticket.email}"); y -= 20
    p.drawString(100, y, f"Status: {ticket.status}")
    p.save()
    pdf_buffer.seek(0)
    return pdf_buffer


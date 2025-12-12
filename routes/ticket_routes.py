from flask import (
    Blueprint, render_template, redirect, url_for, 
    flash, request, current_app
)
from extensions import db, mail
from forms import TicketForm
from models import Ticket
from utils import send_ticket_email
import os
from werkzeug.utils import secure_filename
from datetime import datetime # 1. Import datetime for submitted_at field

ticket_bp = Blueprint('ticket_bp', __name__)

# NOTE: The UPLOAD_FOLDER path should ideally be configured in config.py
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@ticket_bp.route('/', methods=['GET', 'POST'])
def submit_ticket():
    form = TicketForm()
    ticket_submitted = False
    ticket_no = None
    submitted_email = None # 2. Initialize email variable for template context

    if form.validate_on_submit():
        
        # 3. Define current time once for consistency (Ticket No and submitted_at)
        current_time = datetime.utcnow()
        ticket_no = f"T{int(current_time.timestamp())}"

        # Handle attachment
        attachment_filename = None
        if form.attachment.data:
            file = form.attachment.data
            filename = secure_filename(file.filename)
            # Use current_app.root_path for reliable file saving
            file.save(os.path.join(current_app.root_path, UPLOAD_FOLDER, filename))
            attachment_filename = filename

        # 4. Capture submitted email BEFORE clearing form data (if applicable)
        submitted_email = form.email.data

        # Create ticket entry
        ticket = Ticket(
            ticket_no=ticket_no,
            scheme_name=form.scheme_name.data,
            unit_no=form.unit_no.data,
            category=form.category.data,
            message=form.message.data,
            contact_number=form.contact_number.data,
            email=submitted_email, # Use the captured email
            attachment=attachment_filename,
            submitted_at=current_time # 5. Populate the required submitted_at field
        )

        db.session.add(ticket)
        db.session.commit()

        # Send email notification
        send_ticket_email(ticket)

        flash(f'Ticket {ticket_no} submitted successfully!', 'success')
        ticket_submitted = True

    return render_template(
        'submit_ticket.html',
        form=form,
        ticket_submitted=ticket_submitted,
        ticket_no=ticket_no,
        email=submitted_email # 6. Pass the email to the template for confirmation message
    )

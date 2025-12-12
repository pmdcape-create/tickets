from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from extensions import db, mail
from forms import TicketForm
from models import Ticket
from utils import send_ticket_email
import os
from werkzeug.utils import secure_filename

ticket_bp = Blueprint('ticket_bp', __name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@ticket_bp.route('/', methods=['GET', 'POST'])
def submit_ticket():
    form = TicketForm()
    ticket_submitted = False
    ticket_no = None

    if form.validate_on_submit():
        import datetime
        ticket_no = f"T{int(datetime.datetime.utcnow().timestamp())}"

        # Handle attachment
        attachment_filename = None
        if form.attachment.data:
            file = form.attachment.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            attachment_filename = filename

        # Create ticket entry
        ticket = Ticket(
            ticket_no=ticket_no,
            scheme_name=form.scheme_name.data,
            unit_no=form.unit_no.data,
            category=form.category.data,
            message=form.message.data,
            contact_number=form.contact_number.data,
            email=form.email.data,
            attachment=attachment_filename
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
        ticket_no=ticket_no
    )


from flask import Blueprint, render_template, redirect, url_for, request, flash, send_from_directory
from extensions import db
from models import Ticket
import os
from flask import current_app

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

UPLOAD_FOLDER = 'uploads'

# Admin dashboard to view all tickets
@admin_bp.route('/')
def dashboard():
    tickets = Ticket.query.order_by(Ticket.id.desc()).all()
    return render_template('admin_dashboard.html', tickets=tickets)

# Update ticket status
@admin_bp.route('/update/<int:ticket_id>', methods=['POST'])
def update_status(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    new_status = request.form.get('status')
    if new_status in ['Pending', 'In Progress', 'Completed']:
        ticket.status = new_status
        db.session.commit()
        flash(f'Ticket {ticket.ticket_no} status updated to {new_status}', 'success')
    else:
        flash('Invalid status selected', 'danger')
    return redirect(url_for('admin_bp.dashboard'))

# Download ticket attachment
@admin_bp.route('/download/<filename>')
def download_attachment(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

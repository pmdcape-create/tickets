# File: routes/admin_routes.py

import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory
from datetime import datetime
from extensions import db
from models import Ticket   # ← make sure this import works

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

# CHANGE THIS PASSWORD OR SET IT IN RAILWAY VARIABLES !!
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'waltco2025')   # ← change or set in Railway

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            flash('Login successful!', 'success')
            return redirect(url_for('admin_bp.dashboard', auth='true'))
        else:
            flash('Wrong password – try again.', 'danger')

    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Admin Login – Waltco</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%); min-height:100vh; display:flex; align-items:center; justify-content:center; }
            .card { border-radius:16px; box-shadow:0 15px 35px rgba(0,0,0,0.1); }
        </style>
    </head>
    <body>
        <div class="card p-5" style="max-width:420px;">
            <h3 class="text-center mb-4">Admin Login</h3>
            <form method="post">
                <input type="password" name="password" class="form-control form-control-lg" placeholder="Password" required autofocus>
                <button type="submit" class="btn btn-primary btn-lg w-100 mt-4">Login</button>
            </form>
        </div>
    </body>
    </html>
    '''

@admin_bp.route('/dashboard')
def dashboard():
    if request.args.get('auth') != 'true':
        return redirect(url_for('admin_bp.admin_login'))

    tickets = Ticket.query.order_by(Ticket.id.desc()).all()
    return render_template('admin_dashboard.html', tickets=tickets)

@admin_bp.route('/update_status/<int:ticket_id>', methods=['POST'])
def update_status(ticket_id):
    if request.args.get('auth') != 'true':
        return redirect(url_for('admin_bp.admin_login'))

    ticket = Ticket.query.get_or_404(ticket_id)
    new_status = request.form.get('status')
    if new_status in ['Pending', 'In Progress', 'Completed']:
        ticket.status = new_status
        db.session.commit()
        flash(f'Ticket {ticket.ticket_no} → {new_status}', 'success')
    else:
        flash('Invalid status', 'danger')

    return redirect(url_for('admin_bp.dashboard', auth='true'))

@admin_bp.route('/download/<filename>')
def download_attachment(filename):
    if request.args.get('auth') != 'true':
        return redirect(url_for('admin_bp.admin_login'))
    return send_from_directory('uploads', filename, as_attachment=True)

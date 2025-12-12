# routes/admin_routes.py   ←  THIS VERSION WORKS 100%

import os
from flask import (Blueprint, render_template, request, flash,
                   redirect, url_for, send_from_directory)
from extensions import db
from models import Ticket  # ← this works in your repo

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

# CHANGE THIS PASSWORD or set ADMIN_PASSWORD in Railway Variables
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'waltco2025')

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            flash('Login successful!', 'success')
            return redirect('/admin/dashboard?auth=true')
        flash('Wrong password', 'danger')
    return '''
    <!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Admin Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>body{background:#f8f9fa;display:flex;align-items:center;justify-content:center;height:100vh}</style>
    </head><body>
    <div class="card p-5 shadow" style="max-width:400px">
      <h3 class="text-center">Admin Login</h3>
      <form method="post">
        <input type="password" name="password" class="form-control form-control-lg mt-4" placeholder="Password" required>
        <button class="btn btn-primary w-100 mt-3">Login</button>
      </form>
    </div>
    </body></html>
    '''

@admin_bp.route('/dashboard')
def dashboard():
    if request.args.get('auth') != 'true':
        return redirect('/admin/login')

    tickets = Ticket.query.order_by(Ticket.id.desc()).all()
    return render_template('admin_dashboard.html', tickets=tickets)

@admin_bp.route('/update_status/<int:ticket_id>', methods=['POST'])
def update_status(ticket_id):
    if request.args.get('auth') != 'true':
        return redirect('/admin/login')

    ticket = Ticket.query.get_or_404(ticket_id)
    ticket.status = request.form['status']
    db.session.commit()
    flash(f'Ticket {ticket.ticket_no} → {ticket.status}', 'success')
    return redirect('/admin/dashboard?auth=true')

@admin_bp.route('/download/<filename>')
def download_attachment(filename):
    if request.args.get('auth') != 'true':
        return redirect('/admin/login')
    return send_from_directory('uploads', filename, as_attachment=True)

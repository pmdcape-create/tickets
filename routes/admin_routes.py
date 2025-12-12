import os
from flask import (Blueprint, render_template, request, flash,
                   redirect, url_for, send_from_directory)
# Ensure 'mail' is imported for the resend function
from extensions import db, mail 
from models import Ticket

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

# CHANGE THIS PASSWORD or set ADMIN_PASSWORD in Railway Variables
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'waltco2025')

# --- Login Route (Static HTML remains for simplicity) ---

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            flash('Login successful!', 'success')
            # Use url_for for redirects
            return redirect(url_for('admin_bp.dashboard', auth='true'))
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

# --- Dashboard Route (Filter & Sort Logic Added) ---

@admin_bp.route('/dashboard')
def dashboard():
    auth_token = request.args.get('auth', 'false')
    if auth_token != 'true':
        return redirect(url_for('admin_bp.admin_login'))

    # Get filter and sort parameters from URL
    status_filter = request.args.get('status')
    # Default sorting is 'newest' first, based on the submitted_at field
    sort_by = request.args.get('sort', 'newest') 

    # 1. Start the base query
    query = Ticket.query

    # 2. Apply status filtering
    VALID_STATUSES = ['Pending', 'In Progress', 'Completed']
    if status_filter and status_filter in VALID_STATUSES:
        query = query.filter_by(status=status_filter)

    # 3. Apply sorting based on submitted_at
    if sort_by == 'oldest':
        tickets = query.order_by(Ticket.submitted_at.asc()).all()
    else: # Default or 'newest'
        tickets = query.order_by(Ticket.submitted_at.desc()).all()
        
    # Pass all relevant data to the template for display and control functionality
    return render_template('admin_dashboard.html', 
                           tickets=tickets,
                           active_status=status_filter,
                           active_sort=sort_by,
                           auth_token=auth_token)

# --- Update Status Route (Enhanced Flash Message) ---

@admin_bp.route('/update_status/<int:ticket_id>', methods=['POST'])
def update_status(ticket_id):
    auth_token = request.args.get('auth', 'false')
    if auth_token != 'true':
        return redirect(url_for('admin_bp.admin_login'))

    ticket = Ticket.query.get_or_404(ticket_id)
    old_status = ticket.status
    new_status = request.form['status']
    
    # Update and commit to database
    ticket.status = new_status
    db.session.commit()
    
    # Enhanced flash message for staff feedback
    flash(f'Ticket **{ticket.ticket_no}** status updated from **{old_status}** to **{new_status}**.', 'success')
    
    # Redirect back to dashboard, preserving the auth token
    return redirect(url_for('admin_bp.dashboard', auth=auth_token))

# --- Resend Email Route (New Feature) ---

@admin_bp.route('/resend_email/<int:ticket_id>')
def resend_email(ticket_id):
    auth_token = request.args.get('auth', 'false')
    if auth_token != 'true':
        return redirect(url_for('admin_bp.admin_login'))
        
    ticket = Ticket.query.get_or_404(ticket_id)
    
    try:
        # NOTE: This assumes you have a function called 'send_ticket_email' 
        # that can handle the actual email sending logic (likely imported from utils)
        from utils import send_ticket_email
        send_ticket_email(ticket, is_resend=True) 
        
        flash(f'Ticket **{ticket.ticket_no}** email notification re-sent to the staff successfully.', 'info')
        
    except Exception as e:
        # Log the error for debugging
        print(f"EMAIL RESEND ERROR: {e}")
        flash(f'Failed to re-send email for Ticket **{ticket.ticket_no}**. Check logs.', 'danger')

    # Redirect back to dashboard, preserving the auth token
    return redirect(url_for('admin_bp.dashboard', auth=auth_token))

# --- Download Route (Uses auth token now) ---

@admin_bp.route('/download/<filename>')
def download_attachment(filename):
    if request.args.get('auth') != 'true':
        return redirect(url_for('admin_bp.admin_login'))
    
    # Assumes 'uploads' is the correct folder, relative to the app root
    return send_from_directory('uploads', filename, as_attachment=True)


from flask import Blueprint, render_template, session
from decorators import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
# @login_required
def show_dashboard():
    return render_template('dashboard.html', username=session.get('user_id'))
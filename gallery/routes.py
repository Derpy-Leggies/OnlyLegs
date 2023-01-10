from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from gallery.auth import login_required
from gallery.db import get_db

bp = Blueprint('routes', __name__)

#
#   ROUTES
#
@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/group')
def group():
    return render_template('group.html', group_id='gwa gwa')

@bp.route('/group/<group_id>')
def group_id(group_id):
    try:
        group_id = int(group_id)
    except ValueError:
        abort(404)
    
    return render_template('group.html', group_id=group_id)

@bp.route('/upload')
def upload():
    return render_template('upload.html')

@bp.route('/upload/form', methods=['POST'])
def upload_form():
    if request.method != 'POST':
        abort(405)

    return 'balls'

@bp.route('/profile')
def profile():
    return render_template('profile.html', user_id='gwa gwa')

@bp.route('/profile/<user_id>')
def profile_id(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        abort(404)
        
    return render_template('profile.html', user_id=user_id)

@bp.route('/settings')
def settings():
    return render_template('settings.html')

@bp.route('/image/<request_id>')
def image(request_id):
    # Check if request_id is valid
    try:
        request_id = int(request_id)
    except ValueError:
        abort(404)
    
    result = onlylegsDB.getImage(request_id)
    
    return render_template('image.html', fileName=result[1], id=request_id)
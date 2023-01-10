from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from gallery.auth import login_required
from gallery.db import get_db
import json
import os
blueprint = Blueprint('gallery', __name__)


@blueprint.route('/')
def index():
    return render_template('index.html')

@blueprint.route('/image/<request_id>')
def image(request_id):
    # Check if request_id is valid
    try:
        request_id = int(request_id)
    except ValueError:
        abort(404)
    
    result = onlylegsDB.getImage(request_id)
    
    return render_template('image.html', fileName=result[1], id=request_id)


@blueprint.route('/group')
def groups():
    return render_template('groups/group.html', group_id='gwa gwa')

@blueprint.route('/group/<int:id>')
def group(id):    
    return render_template('groups/group.html', group_id=id)


@blueprint.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        form = request.form
        
        if not file:
            flash('No selected file')
            return abort(404)
        
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        
        return json.dumps({'filename': secure_filename(file.filename), 'form': form})
           
    return render_template('upload.html')


@blueprint.route('/profile')
def profile():
    return render_template('profile.html', user_id='gwa gwa')


@blueprint.route('/profile/<int:id>')
def profile_id(id):
    return render_template('profile.html', user_id=id)


@blueprint.route('/settings')
@login_required
def settings():
    return render_template('settings.html')
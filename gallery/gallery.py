from flask import Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, current_app
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from gallery.auth import login_required
from gallery.db import get_db
import os
import datetime
from PIL import Image
from PIL.ExifTags import TAGS
dt = datetime.datetime.now()

blueprint = Blueprint('gallery', __name__)


@blueprint.route('/')
def index():
    db = get_db()
    images = db.execute(
        'SELECT * FROM posts'
        ' ORDER BY created_at DESC'
    ).fetchall()
    
    return render_template('index.html', images=images)

@blueprint.route('/group')
def groups():
    return render_template('group.html', group_id='gwa gwa')

@blueprint.route('/group/<int:id>')
def group(id):    
    return render_template('group.html', group_id=id)


@blueprint.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        form = request.form
        
        if not file:
            flash('No selected file')
            return abort(404)
        if secure_filename(file.filename).lower().split('.')[-1] in current_app.config['ALLOWED_EXTENSIONS']:
            file_name = f"GWAGWA_{dt.year}{dt.month}{dt.day}-{dt.microsecond}.{secure_filename(file.filename).lower().split('.')[-1]}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER']+'/original', file_name))
            
        db = get_db()
        db.execute(
            'INSERT INTO posts (file_name, author_id, description, alt)'
            ' VALUES (?, ?, ?, ?)',
            (file_name, g.user['id'], form['description'], form['alt'])
        )
        db.commit()
        
        return 'Gwa Gwa'

    # GET, or in human language, when you visit the page
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
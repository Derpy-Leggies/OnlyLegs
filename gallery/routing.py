from flask import Blueprint, render_template, current_app
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from gallery.auth import login_required
from gallery.db import get_db

from . import metadata as mt
from PIL import Image

import os
from datetime import datetime

dt = datetime.now()
blueprint = Blueprint('gallery', __name__)


@blueprint.route('/')
def index():
    db = get_db()
    images = db.execute('SELECT * FROM posts'
                        ' ORDER BY created_at DESC').fetchall()

    return render_template('index.html',
                           images=images,
                           image_count=len(images),
                           name=current_app.config['WEBSITE']['name'],
                           motto=current_app.config['WEBSITE']['motto'])


@blueprint.route('/image/<int:id>')
def image(id):
    # Get image from database
    db = get_db()
    image = db.execute('SELECT * FROM posts WHERE id = ?', (id, )).fetchone()

    if image is None:
        abort(404)

    exif = mt.metadata.yoink(
        os.path.join(current_app.config['UPLOAD_FOLDER'], image['file_name']))

    return render_template('image.html', image=image, exif=exif)


@blueprint.route('/group')
def groups():
    return render_template('group.html', group_id='gwa gwa')


@blueprint.route('/group/<int:id>')
def group(id):
    return render_template('group.html', group_id=id)


@blueprint.route('/upload')
@login_required
def upload():
    return render_template('upload.html')


@blueprint.route('/profile')
def profile():
    return render_template('profile.html', user_id='gwa gwa')


@blueprint.route('/profile/<int:id>')
def profile_id(id):
    return render_template('profile.html', user_id=id)
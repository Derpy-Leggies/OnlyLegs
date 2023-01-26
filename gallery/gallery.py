from flask import Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, current_app
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from gallery.auth import login_required
from gallery.db import get_db

from PIL import Image
from PIL.ExifTags import TAGS

import os
import datetime

dt = datetime.datetime.now()

blueprint = Blueprint('gallery', __name__)


@blueprint.route('/')
def index():
    db = get_db()
    images = db.execute('SELECT * FROM posts'
                        ' ORDER BY created_at DESC').fetchall()

    return render_template('index.html', images=images)


@blueprint.route('/image/<int:id>')
def image(id):
    # Get image from database
    db = get_db()
    image = db.execute('SELECT * FROM posts WHERE id = ?', (id, )).fetchone()

    if image is None:
        abort(404)

    # Get exif data from image
    file = Image.open(
        os.path.join(current_app.config['UPLOAD_FOLDER'], image['file_name']))
    raw_exif = file.getexif()
    human_exif = {}

    try:
        for tag in raw_exif:
            name = TAGS.get(tag, tag)
            value = raw_exif.get(tag)

            if isinstance(value, bytes):
                value = value.decode()

            human_exif[name] = value
    except Exception as e:
        human_exif = False

    def human_size(num, suffix="B"):
        for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
            if abs(num) < 1024.0:
                return f"{num:3.1f}{unit}{suffix}"
            num /= 1024.0
        return f"{num:.1f}Yi{suffix}"

    size = os.path.getsize(
        os.path.join(current_app.config['UPLOAD_FOLDER'], image['file_name']))

    # All in le head
    return render_template('image.html',
                           image=image,
                           exif=human_exif,
                           file=file,
                           size=human_size(size))


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


@blueprint.route('/settings')
@login_required
def settings():
    return render_template('settings.html')
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
    image = db.execute('SELECT * FROM posts'
                       ' WHERE id = ?', (id, )).fetchone()

    if image is None:
        abort(404)

    # Get exif data from image
    try:
        file = Image.open(
            os.path.join(current_app.config['UPLOAD_FOLDER'],
                         image['file_name']))
        raw_exif = file.getexif()
        human_exif = {}

        for tag in raw_exif:
            name = TAGS.get(tag, tag)
            value = raw_exif.get(tag)

            if isinstance(value, bytes):
                value = value.decode()

            human_exif[name] = value

        if len(human_exif) == 0:
            human_exif = False
    except:
        # Cringe, no file present
        human_exif = False
        file = False

    # All in le head
    return render_template('image.html',
                           image=image,
                           exif=human_exif,
                           file=file)


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
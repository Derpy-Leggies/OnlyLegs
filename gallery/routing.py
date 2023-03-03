from flask import Blueprint, render_template, current_app
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from gallery.auth import login_required

from . import db
from sqlalchemy.orm import sessionmaker
db_session = sessionmaker(bind=db.engine)
db_session = db_session()

from . import metadata as mt

import os

blueprint = Blueprint('gallery', __name__)


@blueprint.route('/')
def index():
    images = db_session.query(db.posts).order_by(db.posts.id.desc()).all()

    return render_template('index.html',
                           images=images,
                           image_count=len(images),
                           name=current_app.config['WEBSITE']['name'],
                           motto=current_app.config['WEBSITE']['motto'])


@blueprint.route('/image/<int:id>')
def image(id):
    img = db_session.query(db.posts).filter_by(id=id).first()

    if img is None:
        abort(404)

    exif = mt.metadata.yoink(
        os.path.join(current_app.config['UPLOAD_FOLDER'], img.file_name))

    return render_template('image.html', image=img, exif=exif)


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
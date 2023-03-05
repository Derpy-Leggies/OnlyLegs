"""
Onlylegs Gallery - Routing
"""
import os

from flask import Blueprint, render_template, current_app
from werkzeug.exceptions import abort

from sqlalchemy.orm import sessionmaker

from . import db
from . import metadata as mt


blueprint = Blueprint('gallery', __name__)
db_session = sessionmaker(bind=db.engine)
db_session = db_session()


@blueprint.route('/')
def index():
    """
    Home page of the website, shows the feed of latest images
    """
    images = db_session.query(db.Posts.file_name, db.Posts.id, db.Posts.created_at).order_by(db.Posts.id.desc()).all()
 
    return render_template('index.html',
                           images=images,
                           image_count=len(images),
                           name=current_app.config['WEBSITE']['name'],
                           motto=current_app.config['WEBSITE']['motto'])

@blueprint.route('/image/<int:image_id>')
def image(image_id):
    """
    Image view, shows the image and its metadata
    """
    img = db_session.query(db.Posts).filter_by(id=image_id).first()

    if img is None:
        abort(404)

    return render_template('image.html', image=img, exif=img.image_exif)

@blueprint.route('/group')
def groups():
    """
    Group overview, shows all image groups
    """
    return render_template('group.html', group_id='gwa gwa')

@blueprint.route('/group/<int:group_id>')
def group(group_id):
    """
    Group view, shows all images in a group
    """
    return render_template('group.html', group_id=group_id)

@blueprint.route('/profile')
def profile():
    """
    Profile overview, shows all profiles on the onlylegs gallery
    """
    return render_template('profile.html', user_id='gwa gwa')

@blueprint.route('/profile/<int:user_id>')
def profile_id(user_id):
    """
    Shows user ofa given id, displays their uploads and other info
    """
    return render_template('profile.html', user_id=user_id)

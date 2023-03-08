"""
Onlylegs Gallery - Routing
"""
import os
from datetime import datetime as dt

from flask import Blueprint, render_template, current_app, request, g
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
    images = db_session.query(db.Posts.file_name,
                              db.Posts.image_colours,
                              db.Posts.author_id,
                              db.Posts.created_at,
                              db.Posts.id).order_by(db.Posts.id.desc()).all()
 
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
    img = db_session.query(db.Posts).filter(db.Posts.id == image_id).first()
    author = db_session.query(db.Users.username).filter(db.Users.id == img.author_id).first()[0]
    img.author_username = author
    
    if img is None:
        abort(404, 'Image not found')

    return render_template('image.html', image=img, exif=img.image_exif)

@blueprint.route('/group', methods=['GET', 'POST'])
def groups():
    """
    Group overview, shows all image groups
    """
    if request.method == 'GET':
        groups = db_session.query(db.Groups.name, db.Groups.author_id).all()
        
        return render_template('group.html', groups=groups)
    elif request.method == 'POST':
        group_name = request.form['name']
        group_description = request.form['description']
        group_author = g.user.id
        
        new_group = db.Groups(name=group_name, description=group_description, author_id=group_author, created_at=dt.now())
        
        db_session.add(new_group)
        
        return ':3'

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
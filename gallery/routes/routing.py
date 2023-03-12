"""
Onlylegs Gallery - Routing
"""
from datetime import datetime as dt

from flask import Blueprint, render_template, url_for
from werkzeug.exceptions import abort

from sqlalchemy.orm import sessionmaker
from gallery import db


blueprint = Blueprint('gallery', __name__)
db_session = sessionmaker(bind=db.engine)
db_session = db_session()


@blueprint.route('/')
def index():
    """
    Home page of the website, shows the feed of the latest images
    """
    images = db_session.query(db.Posts.file_name,
                              db.Posts.post_alt,
                              db.Posts.image_colours,
                              db.Posts.created_at,
                              db.Posts.id).order_by(db.Posts.id.desc()).all()
 
    return render_template('index.html', images=images)


@blueprint.route('/image/<int:image_id>')
def image(image_id):
    """
    Image view, shows the image and its metadata
    """
    img = db_session.query(db.Posts).filter(db.Posts.id == image_id).first()

    if img is None:
        abort(404, 'Image not found :<')

    img.author_username = db_session.query(db.Users.username).filter(db.Users.id == img.author_id).first()[0]
    
    groups = db_session.query(db.GroupJunction.group_id).filter(db.GroupJunction.post_id == image_id).all()
    img.groups = []
    for group in groups:
        group = db_session.query(db.Groups).filter(db.Groups.id == group[0]).first()
        img.groups.append(group)
    
    next_url = db_session.query(db.Posts.id).filter(db.Posts.id > image_id).order_by(db.Posts.id.asc()).first()
    prev_url = db_session.query(db.Posts.id).filter(db.Posts.id < image_id).order_by(db.Posts.id.desc()).first()
    
    if next_url is not None:
        next_url = url_for('gallery.image', image_id=next_url[0])
    if prev_url is not None:
        prev_url = url_for('gallery.image', image_id=prev_url[0])

    return render_template('image.html', image=img, next_url=next_url, prev_url=prev_url)


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

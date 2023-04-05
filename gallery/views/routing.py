"""
Onlylegs Gallery - Routing
"""
from flask import Blueprint, render_template, url_for, request
from werkzeug.exceptions import abort
from flask_login import current_user

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
    images = db_session.query(db.Posts.filename,
                              db.Posts.alt,
                              db.Posts.colours,
                              db.Posts.created_at,
                              db.Posts.id).order_by(db.Posts.id.desc()).all()

    if request.args.get('coffee') == 'please':
        abort(418)

    return render_template('index.html', images=images)


@blueprint.route('/image/<int:image_id>')
def image(image_id):
    """
    Image view, shows the image and its metadata
    """
    # Get the image, if it doesn't exist, 404
    image = db_session.query(db.Posts).filter(db.Posts.id == image_id).first()
    if not image:
        abort(404, 'Image not found :<')

    # Get the image's author username
    image.author_username = (db_session.query(db.Users.username)
                                       .filter(db.Users.id == image.author_id)
                                       .first()[0])

    # Get the image's groups
    groups = (db_session.query(db.GroupJunction.group_id)
                        .filter(db.GroupJunction.post_id == image_id)
                        .all())

    # For each group, get the group data and add it to the image item
    image.groups = []
    for group in groups:
        image.groups.append(db_session.query(db.Groups.id, db.Groups.name)
                                      .filter(db.Groups.id == group[0])
                                      .first())

    # Get the next and previous images
    next_url = (db_session.query(db.Posts.id)
                          .filter(db.Posts.id > image_id)
                          .order_by(db.Posts.id.asc())
                          .first())
    prev_url = (db_session.query(db.Posts.id)
                          .filter(db.Posts.id < image_id)
                          .order_by(db.Posts.id.desc())
                          .first())

    # If there is a next or previous image, get the url
    if next_url:
        next_url = url_for('gallery.image', image_id=next_url[0])
    if prev_url:
        prev_url = url_for('gallery.image', image_id=prev_url[0])

    return render_template('image.html', image=image, next_url=next_url, prev_url=prev_url)


@blueprint.route('/profile')
def profile():
    """
    Profile overview, shows all profiles on the onlylegs gallery
    """
    user_id = request.args.get('id', default=None, type=int)

    # If there is no userID set, check if the user is logged in and display their profile
    if not user_id:
        if current_user.is_authenticated:
            user_id = current_user.id
        else:
            abort(404, 'You must be logged in to view your own profile!')

    # Get the user's data
    user = db_session.query(db.Users).filter(db.Users.id == user_id).first()

    if not user:
        abort(404, 'User not found :c')

    images = db_session.query(db.Posts).filter(db.Posts.author_id == user_id).all()

    return render_template('profile.html', user=user, images=images)

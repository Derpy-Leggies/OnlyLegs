"""
Onlylegs - Image View
"""
from flask import Blueprint, abort, render_template, url_for

from sqlalchemy.orm import sessionmaker
from gallery import db


blueprint = Blueprint('image', __name__, url_prefix='/image')
db_session = sessionmaker(bind=db.engine)
db_session = db_session()


@blueprint.route('/<int:image_id>')
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
    # Check if there is a group ID set
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
        next_url = url_for('image.image', image_id=next_url[0])
    if prev_url:
        prev_url = url_for('image.image', image_id=prev_url[0])

    return render_template('image.html', image=image, next_url=next_url, prev_url=prev_url)

"""
Onlylegs - Image Groups
Why groups? Because I don't like calling these albums
sounds more limiting that it actually is in this gallery
"""
from flask import Blueprint, abort, render_template, url_for

from sqlalchemy.orm import sessionmaker
from gallery import db
from gallery.utils import contrast


blueprint = Blueprint('group', __name__, url_prefix='/group')
db_session = sessionmaker(bind=db.engine)
db_session = db_session()


@blueprint.route('/', methods=['GET'])
def groups():
    """
    Group overview, shows all image groups
    """
    groups = db_session.query(db.Groups).all()

    # For each group, get the 3 most recent images
    for group in groups:
        group.author_username = (db_session.query(db.Users.username)
                                           .filter(db.Users.id == group.author_id)
                                           .first()[0])

        # Get the 3 most recent images
        images = (db_session.query(db.GroupJunction.post_id)
                            .filter(db.GroupJunction.group_id == group.id)
                            .order_by(db.GroupJunction.date_added.desc())
                            .limit(3))

        # For each image, get the image data and add it to the group item
        group.images = []
        for image in images:
            group.images.append(db_session.query(db.Posts.filename, db.Posts.alt,
                                                 db.Posts.colours, db.Posts.id)
                                          .filter(db.Posts.id == image[0])
                                          .first())

    return render_template('list.html', groups=groups)


@blueprint.route('/<int:group_id>')
def group(group_id):
    """
    Group view, shows all images in a group
    """
    # Get the group, if it doesn't exist, 404
    group = (db_session.query(db.Groups)
                       .filter(db.Groups.id == group_id)
                       .first())

    if group is None:
        abort(404, 'Group not found! D:')

    # Get the group's author username
    group.author_username = (db_session.query(db.Users.username)
                                       .filter(db.Users.id == group.author_id)
                                       .first()[0])

    # Get all images in the group from the junction table
    junction = (db_session.query(db.GroupJunction.post_id)
                          .filter(db.GroupJunction.group_id == group_id)
                          .order_by(db.GroupJunction.date_added.desc())
                          .all())

    # Get the image data for each image in the group
    images = []
    for image in junction:
        images.append(db_session.query(db.Posts)
                                .filter(db.Posts.id == image[0])
                                .first())

    # Check contrast for the first image in the group for the banner
    text_colour = 'rgb(var(--fg-black))'
    if images:
        text_colour = contrast.contrast(images[0].colours[0],
                                        'rgb(var(--fg-black))',
                                        'rgb(var(--fg-white))')

    return render_template('group.html',
                           group=group,
                           images=images,
                           text_colour=text_colour)


@blueprint.route('/<int:group_id>/<int:image_id>')
def group_post(group_id, image_id):
    """
    Image view, shows the image and its metadata from a specific group
    """
    # Get the image, if it doesn't exist, 404
    image = (db_session.query(db.Posts)
                       .filter(db.Posts.id == image_id)
                       .first())
    if image is None:
        abort(404, 'Image not found')

    # Get the image's author username
    image.author_username = (db_session.query(db.Users.username)
                                       .filter(db.Users.id == image.author_id)
                                       .first()[0])

    # Get all groups the image is in
    groups = (db_session.query(db.GroupJunction.group_id)
                        .filter(db.GroupJunction.post_id == image_id)
                        .all())

    # Get the group data for each group the image is in
    image.groups = []
    for group in groups:
        image.groups.append(db_session.query(db.Groups.id, db.Groups.name)
                                      .filter(db.Groups.id == group[0])
                                      .first())

    # Get the next and previous images in the group
    next_url = (db_session.query(db.GroupJunction.post_id)
                          .filter(db.GroupJunction.group_id == group_id)
                          .filter(db.GroupJunction.post_id > image_id)
                          .order_by(db.GroupJunction.date_added.asc())
                          .first())
    prev_url = (db_session.query(db.GroupJunction.post_id)
                          .filter(db.GroupJunction.group_id == group_id)
                          .filter(db.GroupJunction.post_id < image_id)
                          .order_by(db.GroupJunction.date_added.desc())
                          .first())

    # If there is a next or previous image, get the URL for it
    if next_url:
        next_url = url_for('group.group_post', group_id=group_id, image_id=next_url[0])
    if prev_url:
        prev_url = url_for('group.group_post', group_id=group_id, image_id=prev_url[0])

    return render_template('image.html', image=image, next_url=next_url,
                           prev_url=prev_url, return_page=0)

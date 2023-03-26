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
    group_list = db_session.query(db.Groups).all()

    for group_item in group_list:
        thumbnail = db_session.query(db.GroupJunction.post_id)\
                              .filter(db.GroupJunction.group_id == group_item.id)\
                              .order_by(db.GroupJunction.date_added.desc())\
                              .first()

        if thumbnail:
            group_item.thumbnail = db_session.query(db.Posts.file_name, db.Posts.post_alt,
                                               db.Posts.image_colours, db.Posts.id)\
                                        .filter(db.Posts.id == thumbnail[0])\
                                        .first()

    return render_template('groups/list.html', groups=group_list)


@blueprint.route('/<int:group_id>')
def group(group_id):
    """
    Group view, shows all images in a group
    """
    group_item = db_session.query(db.Groups).filter(db.Groups.id == group_id).first()

    if group_item is None:
        abort(404, 'Group not found! D:')

    group_item.author_username = db_session.query(db.Users.username)\
                                           .filter(db.Users.id == group_item.author_id)\
                                           .first()[0]

    group_images = db_session.query(db.GroupJunction.post_id)\
                             .filter(db.GroupJunction.group_id == group_id)\
                             .order_by(db.GroupJunction.date_added.desc())\
                             .all()

    images = []
    for image in group_images:
        image = db_session.query(db.Posts).filter(db.Posts.id == image[0]).first()
        images.append(image)
    
    if images:
        text_colour = contrast.contrast(images[0].image_colours[0], 'rgb(var(--fg-black))', 'rgb(var(--fg-white))')
    else:
        text_colour = 'rgb(var(--fg-black))'

    return render_template('groups/group.html', group=group_item, images=images, text_colour=text_colour)


@blueprint.route('/<int:group_id>/<int:image_id>')
def group_post(group_id, image_id):
    """
    Image view, shows the image and its metadata from a specific group
    """
    img = db_session.query(db.Posts).filter(db.Posts.id == image_id).first()

    if img is None:
        abort(404, 'Image not found')

    img.author_username = db_session.query(db.Users.username)\
                                    .filter(db.Users.id == img.author_id)\
                                    .first()[0]

    group_list = db_session.query(db.GroupJunction.group_id)\
                       .filter(db.GroupJunction.post_id == image_id)\
                       .all()

    img.group_list = []
    for group_item in group_list:
        group_item = db_session.query(db.Groups).filter(db.Groups.id == group_item[0]).first()
        img.group_list.append(group_item)

    next_url = db_session.query(db.GroupJunction.post_id)\
                         .filter(db.GroupJunction.group_id == group_id)\
                         .filter(db.GroupJunction.post_id > image_id)\
                         .order_by(db.GroupJunction.date_added.asc())\
                         .first()

    prev_url = db_session.query(db.GroupJunction.post_id)\
                         .filter(db.GroupJunction.group_id == group_id)\
                         .filter(db.GroupJunction.post_id < image_id)\
                         .order_by(db.GroupJunction.date_added.desc())\
                         .first()

    if next_url is not None:
        next_url = url_for('group.group_post', group_id=group_id, image_id=next_url[0])
    if prev_url is not None:
        prev_url = url_for('group.group_post', group_id=group_id, image_id=prev_url[0])

    return render_template('image.html', image=img, next_url=next_url, prev_url=prev_url)

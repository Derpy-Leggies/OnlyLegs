"""
Onlylegs - Image Groups
Why groups? Because I don't like calling these albums, sounds more limiting that it actually is
"""
import logging
import json
from datetime import datetime as dt

from flask import Blueprint, abort, jsonify, render_template, url_for, request, g

from sqlalchemy.orm import sessionmaker
from gallery import db


blueprint = Blueprint('group', __name__, url_prefix='/group')
db_session = sessionmaker(bind=db.engine)
db_session = db_session()


@blueprint.route('/', methods=['GET'])
def groups():
    """
    Group overview, shows all image groups
    """
    groups = db_session.query(db.Groups).all()
    
    for group in groups:
        thumbnail = db_session.query(db.GroupJunction.post_id).filter(db.GroupJunction.group_id == group.id).order_by(db.GroupJunction.date_added.desc()).first()
        
        if thumbnail is not None:
            group.thumbnail = db_session.query(db.Posts.file_name, db.Posts.post_alt, db.Posts.image_colours, db.Posts.id).filter(db.Posts.id == thumbnail[0]).first()
    
    return render_template('groups/list.html', groups=groups)


@blueprint.route('/<int:group_id>')
def group(group_id):
    """
    Group view, shows all images in a group
    """
    group = db_session.query(db.Groups).filter(db.Groups.id == group_id).first()
    
    if group is None:
        abort(404, 'Group not found! D:')
        
    group.author_username = db_session.query(db.Users.username).filter(db.Users.id == group.author_id).first()[0]
    
    group_images = db_session.query(db.GroupJunction.post_id).filter(db.GroupJunction.group_id == group_id).order_by(db.GroupJunction.date_added.desc()).all()
    
    images = []
    for image in group_images:
        image = db_session.query(db.Posts).filter(db.Posts.id == image[0]).first()
        images.append(image)
    
    return render_template('groups/group.html', group=group, images=images)


@blueprint.route('/<int:group_id>/<int:image_id>')
def group_post(group_id, image_id):
    """
    Image view, shows the image and its metadata from a specific group
    """
    img = db_session.query(db.Posts).filter(db.Posts.id == image_id).first()

    if img is None:
        abort(404, 'Image not found')

    img.author_username = db_session.query(db.Users.username).filter(db.Users.id == img.author_id).first()[0]
    
    groups = db_session.query(db.GroupJunction.group_id).filter(db.GroupJunction.post_id == image_id).all()
    img.groups = []
    for group in groups:
        group = db_session.query(db.Groups).filter(db.Groups.id == group[0]).first()
        img.groups.append(group)
    
    next_url = db_session.query(db.GroupJunction.post_id).filter(db.GroupJunction.group_id == group_id).filter(db.GroupJunction.post_id > image_id).order_by(db.GroupJunction.date_added.asc()).first()    
    prev_url = db_session.query(db.GroupJunction.post_id).filter(db.GroupJunction.group_id == group_id).filter(db.GroupJunction.post_id < image_id).order_by(db.GroupJunction.date_added.desc()).first()
    
    if next_url is not None:
        next_url = url_for('group.group_post', group_id=group_id, image_id=next_url[0])
    if prev_url is not None:
        prev_url = url_for('group.group_post', group_id=group_id, image_id=prev_url[0])

    return render_template('image.html', image=img, next_url=next_url, prev_url=prev_url)

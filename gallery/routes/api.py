"""
Onlylegs - API endpoints
"""
from uuid import uuid4
import os
import pathlib
import logging
from datetime import datetime as dt
import platformdirs

from flask import Blueprint, send_from_directory, abort, flash, jsonify, request, g, current_app
from werkzeug.utils import secure_filename

from colorthief import ColorThief

from sqlalchemy.orm import sessionmaker
from gallery.auth import login_required

from gallery import db
from gallery.utils import metadata as mt
from gallery.utils.generate_image import generate_thumbnail


blueprint = Blueprint('api', __name__, url_prefix='/api')
db_session = sessionmaker(bind=db.engine)
db_session = db_session()


@blueprint.route('/file/<file_name>', methods=['GET'])
def file(file_name):
    """
    Returns a file from the uploads folder
    r for resolution, 400x400 or thumb for thumbnail
    """
    res = request.args.get('r', default=None, type=str)  # Type of file (thumb, etc)
    ext = request.args.get('e', default=None, type=str)  # File extension
    file_name = secure_filename(file_name)  # Sanitize file name

    # if no args are passed, return the raw file
    if not request.args:
        if not os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], file_name)):
            abort(404)
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], file_name)

    thumb = generate_thumbnail(file_name, res, ext)
    if not thumb:
        abort(404)

    return send_from_directory(os.path.dirname(thumb), os.path.basename(thumb))


@blueprint.route('/upload', methods=['POST'])
@login_required
def upload():
    """
    Uploads an image to the server and saves it to the database
    """
    form_file = request.files['file']
    form = request.form

    # If no image is uploaded, return 404 error
    if not form_file:
        return abort(404)

    # Get file extension, generate random name and set file path
    img_ext = pathlib.Path(form_file.filename).suffix.replace('.', '').lower()
    img_name = "GWAGWA_"+str(uuid4())
    img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], img_name+'.'+img_ext)

    # Check if file extension is allowed
    if img_ext not in current_app.config['ALLOWED_EXTENSIONS'].keys():
        logging.info('File extension not allowed: %s', img_ext)
        abort(403)

    # Save file
    try:
        form_file.save(img_path)
    except OSError as err:
        logging.info('Error saving file %s because of %s', img_path, err)
        abort(500)

    img_exif = mt.Metadata(img_path).yoink()  # Get EXIF data
    img_colors = ColorThief(img_path).get_palette(color_count=3)  # Get color palette

    # Save to database
    query = db.Posts(author_id=g.user.id,
                     created_at=dt.utcnow(),
                     file_name=img_name+'.'+img_ext,
                     file_type=img_ext,
                     image_exif=img_exif,
                     image_colours=img_colors,
                     post_description=form['description'],
                     post_alt=form['alt'])

    db_session.add(query)
    db_session.commit()

    return 'Gwa Gwa'  # Return something so the browser doesn't show an error


@blueprint.route('/delete/<int:image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
    """
    Deletes an image from the server and database
    """
    img = db_session.query(db.Posts).filter_by(id=image_id).first()

    # Check if image exists and if user is allowed to delete it (author)
    if img is None:
        abort(404)
    if img.author_id != g.user.id:
        abort(403)

    # Delete file
    try:
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], img.file_name))
    except FileNotFoundError:
        logging.warning('File not found: %s, already deleted or never existed', img.file_name)

    # Delete cached files
    cache_path = os.path.join(platformdirs.user_config_dir('onlylegs'), 'cache')
    cache_name = img.file_name.rsplit('.')[0]
    for cache_file in pathlib.Path(cache_path).glob(cache_name + '*'):
        os.remove(cache_file)

    # Delete from database
    db_session.query(db.Posts).filter_by(id=image_id).delete()

    # Remove all entries in junction table
    groups = db_session.query(db.GroupJunction).filter_by(post_id=image_id).all()
    for group in groups:
        db_session.delete(group)

    # Commit all changes
    db_session.commit()

    logging.info('Removed image (%s) %s', image_id, img.file_name)
    flash(['Image was all in Le Head!', '1'])
    return 'Gwa Gwa'


@blueprint.route('/group/create', methods=['POST'])
@login_required
def create_group():
    """
    Creates a group
    """
    new_group = db.Groups(name=request.form['name'],
                          description=request.form['description'],
                          author_id=g.user.id,
                          created_at=dt.utcnow())

    db_session.add(new_group)
    db_session.commit()

    return ':3'


@blueprint.route('/group/modify', methods=['POST'])
@login_required
def modify_group():
    """
    Changes the images in a group
    """
    group_id = request.form['group']
    image_id = request.form['image']

    group = db_session.query(db.Groups).filter_by(id=group_id).first()

    if group is None:
        abort(404)
    elif group.author_id != g.user.id:
        abort(403)

    if request.form['action'] == 'add':
        if not (db_session.query(db.GroupJunction)
                          .filter_by(group_id=group_id, post_id=image_id)
                          .first()):
            db_session.add(db.GroupJunction(group_id=group_id,
                                            post_id=image_id,
                                            date_added=dt.utcnow()))
    elif request.form['action'] == 'remove':
        (db_session.query(db.GroupJunction)
                   .filter_by(group_id=group_id, post_id=image_id)
                   .delete())

    db_session.commit()

    return ':3'


@blueprint.route('/metadata/<int:img_id>', methods=['GET'])
def metadata(img_id):
    """
    Yoinks metadata from an image
    """
    img = db_session.query(db.Posts).filter_by(id=img_id).first()

    if not img:
        abort(404)

    img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], img.file_name)
    exif = mt.Metadata(img_path).yoink()

    return jsonify(exif)

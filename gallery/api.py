"""
Onlylegs - API endpoints
Used intermally by the frontend and possibly by other applications
"""
from uuid import uuid4
import os
import io
import logging
import json
from datetime import datetime as dt

from flask import (
    Blueprint, send_from_directory, send_file, abort, flash, jsonify, request, g, current_app)
from werkzeug.utils import secure_filename

from colorthief import ColorThief
from PIL import Image, ImageOps, ImageFilter
from sqlalchemy.orm import sessionmaker

from gallery.auth import login_required

from . import db # Import db to create a session
from . import metadata as mt


blueprint = Blueprint('api', __name__, url_prefix='/api')
db_session = sessionmaker(bind=db.engine)
db_session = db_session()


@blueprint.route('/uploads/<file>', methods=['GET'])
def uploads(file):
    """
    Returns a file from the uploads folder
    w and h are the width and height of the image for resizing
    f is whether to apply filters to the image, such as blurring NSFW images
    b is whether to force blur the image, even if it's not NSFW
    """
    # Get args
    width = request.args.get('w', default=0, type=int)  # Width of image
    height = request.args.get('h', default=0, type=int)  # Height of image
    filtered = request.args.get('f', default=False, type=bool) # Whether to apply filters
    blur = request.args.get('b', default=False, type=bool) # Whether to force blur

    # if no args are passed, return the raw file
    if width == 0 and height == 0 and not filtered:
        if not os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'],
                                           secure_filename(file))):
            abort(404)
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], file ,as_attachment=True)

    # Of either width or height is 0, set it to the other value to keep aspect ratio
    if width > 0 and height == 0:
        height = width
    elif width == 0 and height > 0:
        width = height

    set_ext = current_app.config['ALLOWED_EXTENSIONS']
    buff = io.BytesIO()

    # Open image and set extension
    try:
        img = Image.open(os.path.join(current_app.config['UPLOAD_FOLDER'],file))
    except FileNotFoundError:
        logging.error('File not found: %s, possibly broken upload', file)
        abort(404)
    except Exception as err:
        logging.error('Error opening image: %s', err)
        abort(500)

    img_ext = os.path.splitext(file)[-1].lower().replace('.', '')
    img_ext = set_ext[img_ext]
    # Get ICC profile as it alters colours when saving
    img_icc = img.info.get("icc_profile")

    # Resize image and orientate correctly
    img.thumbnail((width, height), Image.LANCZOS)
    img = ImageOps.exif_transpose(img)

    # If has NSFW tag, blur image, etc.
    if filtered:
        #img = img.filter(ImageFilter.GaussianBlur(20))
        pass
    
    # If forced to blur, blur image
    if blur:
        img = img.filter(ImageFilter.GaussianBlur(20))

    try:
        img.save(buff, img_ext, icc_profile=img_icc)
    except OSError:
        # This usually happens when saving a JPEG with an ICC profile
        # Convert to RGB and try again
        img = img.convert('RGB')
        img.save(buff, img_ext, icc_profile=img_icc)
    except Exception as err:
        logging.error('Could not resize image %s, error: %s', file, err)
        abort(500)

    img.close()

    # Seek to beginning of buffer and return
    buff.seek(0)
    return send_file(buff, mimetype='image/' + img_ext)


@blueprint.route('/upload', methods=['POST'])
@login_required
def upload():
    """
    Uploads an image to the server and saves it to the database
    """
    form_file = request.files['file']
    form = request.form
    form_description = form['description']
    form_alt = form['alt']

    if not form_file:
        return abort(404)

    img_ext = os.path.splitext(form_file.filename)[-1].replace('.', '').lower()
    img_name = "GWAGWA_"+str(uuid4())
    img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], img_name+'.'+img_ext)

    if not img_ext in current_app.config['ALLOWED_EXTENSIONS'].keys():
        logging.info('File extension not allowed: %s', img_ext)
        abort(403)

    if os.path.isdir(current_app.config['UPLOAD_FOLDER']) is False:
        os.mkdir(current_app.config['UPLOAD_FOLDER'])

    # Save file
    try:
        form_file.save(img_path)
    except Exception as err:
        logging.error('Could not save file: %s', err)
        abort(500)

    # Get metadata and colors
    img_exif = mt.Metadata(img_path).yoink()
    img_colors = ColorThief(img_path).get_palette(color_count=3)
    
    # Save to database
    try:        
        query = db.Posts(author_id = g.user.id,
                              created_at = dt.utcnow(),
                              file_name = img_name+'.'+img_ext,
                              file_type = img_ext,
                              image_exif = img_exif,
                              image_colours = img_colors,
                              post_description = form_description,
                              post_alt = form_alt)
        
        db_session.add(query)
        db_session.commit()
    except Exception as err:
        logging.error('Could not save to database: %s', err)
        abort(500)

    return 'Gwa Gwa'

@blueprint.route('/delete/<int:image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
    """
    Deletes an image from the server and database
    """
    img = db_session.query(db.Posts).filter_by(id=image_id).first()

    if img is None:
        abort(404)
    if img.author_id != g.user.id:
        abort(403)

    try:
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'],img.file_name))
    except FileNotFoundError:
        # File was already deleted or doesn't exist
        logging.warning('File not found: %s, already deleted or never existed', img.file_name)
    except Exception as err:
        logging.error('Could not remove file: %s', err)
        abort(500)

    try:
        db_session.query(db.Posts).filter_by(id=image_id).delete()
        
        groups = db_session.query(db.GroupJunction).filter_by(post_id=image_id).all()
        for group in groups:
            db_session.delete(group)
        
        db_session.commit()
    except Exception as err:
        logging.error('Could not remove from database: %s', err)
        abort(500)

    logging.info('Removed image (%s) %s', image_id, img.file_name)
    flash(['Image was all in Le Head!', 1])
    return 'Gwa Gwa'


@blueprint.route('/group/create', methods=['POST'])
@login_required
def create_group():
    """
    Creates a group
    """
    group_name = request.form['name']
    group_description = request.form['description']
    group_author = g.user.id
    
    new_group = db.Groups(name=group_name,
                          description=group_description,
                          author_id=group_author,
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
        if db_session.query(db.GroupJunction).filter_by(group_id=group_id, post_id=image_id).first() is None:
            db_session.add(db.GroupJunction(group_id=group_id, post_id=image_id, date_added=dt.utcnow()))
    elif request.form['action'] == 'remove':
        db_session.query(db.GroupJunction).filter_by(group_id=group_id, post_id=image_id).delete()
        
    db_session.commit()
    
    return ':3'


@blueprint.route('/metadata/<int:img_id>', methods=['GET'])
def metadata(img_id):
    """
    Yoinks metadata from an image
    """
    img = db_session.query(db.Posts).filter_by(id=img_id).first()

    if img is None:
        abort(404)

    img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], img.file_name)
    exif = mt.Metadata(img_path).yoink()

    return jsonify(exif)


@blueprint.route('/logfile')
@login_required
def logfile():
    """
    Gets the log file and returns it as a JSON object
    """
    filename = logging.getLoggerClass().root.handlers[0].baseFilename
    log_dict = {}
    i = 0

    with open(filename, encoding='utf-8') as file:
        for line in file:
            line = line.split(' : ')

            event = line[0].strip().split(' ')
            event_data = {
                'date': event[0],
                'time': event[1],
                'severity': event[2],
                'owner': event[3]
            }

            message = line[1].strip()
            try:
                message_data = {
                    'code': int(message[1:4]),
                    'message': message[5:].strip()
                }
            except ValueError:
                message_data = {'code': 0, 'message': message}
            except Exception as err:
                logging.error('Could not parse log file: %s', err)
                abort(500)

            log_dict[i] = {'event': event_data, 'message': message_data}

            i += 1  # Line number, starts at 0

    return jsonify(log_dict)

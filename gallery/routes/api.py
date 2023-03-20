"""
Onlylegs - API endpoints
Used internally by the frontend and possibly by other applications
"""
from uuid import uuid4
import os
import pathlib
import io
import logging
from datetime import datetime as dt

from flask import (Blueprint, send_from_directory, send_file,
                   abort, flash, jsonify, request, g, current_app)
from werkzeug.utils import secure_filename

from colorthief import ColorThief
from PIL import Image, ImageOps, ImageFilter

from sqlalchemy.orm import sessionmaker
from gallery.auth import login_required

from gallery import db
from gallery.utils import metadata as mt


blueprint = Blueprint('api', __name__, url_prefix='/api')
db_session = sessionmaker(bind=db.engine)
db_session = db_session()


@blueprint.route('/file/<file_name>', methods=['GET'])
def get_file(file_name):
    """
    Returns a file from the uploads folder
    r for resolution, 400x400 or thumb for thumbnail
    f is whether to apply filters to the image, such as blurring NSFW images
    b is whether to force blur the image, even if it's not NSFW
    """
    # Get args
    res = request.args.get('r', default=None, type=str)  # Type of file (thumb, etc)
    filtered = request.args.get('f', default=False, type=bool)  # Whether to apply filters  # pylint: disable=W0612
    blur = request.args.get('b', default=False, type=bool)  # Whether to force blur

    file_name = secure_filename(file_name)  # Sanitize file name

    # if no args are passed, return the raw file
    if not request.args:
        if not os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], file_name)):
            abort(404)

        return send_from_directory(current_app.config['UPLOAD_FOLDER'], file_name)

    buff = io.BytesIO()
    img = None  # Image object to be set

    try:  # Open image and set extension
        img = Image.open(os.path.join(current_app.config['UPLOAD_FOLDER'], file_name))
    except FileNotFoundError:  # FileNotFound is raised if the file doesn't exist
        logging.error('File not found: %s', file_name)
        abort(404)
    except OSError as err:  # OSError is raised if the file is broken or corrupted
        logging.error('Possibly broken image %s, error: %s', file_name, err)
        abort(500)

    img_ext = pathlib.Path(file_name).suffix.replace('.', '').lower()  # Get file extension
    img_ext = current_app.config['ALLOWED_EXTENSIONS'][img_ext]  # Convert to MIME type
    img_icc = img.info.get("icc_profile")  # Get ICC profile

    img = ImageOps.exif_transpose(img)  # Rotate image based on EXIF data

    # Todo: If type is thumb(nail), return from database instead of file system  pylint: disable=W0511
    #  as it's faster than generating a new thumbnail on every request
    if res:
        if res in ['thumb', 'thumbnail']:
            width, height = 400, 400
        elif res in ['prev', 'preview']:
            width, height = 1920, 1080
        else:
            try:
                width, height = res.split('x')
                width = int(width)
                height = int(height)
            except ValueError:
                abort(400)

        img.thumbnail((width, height), Image.LANCZOS)

    # Todo: If the image has a NSFW tag, blur image for example  pylint: disable=W0511
    # if filtered:
    #     pass

    # If forced to blur, blur image
    if blur:
        img = img.filter(ImageFilter.GaussianBlur(20))

    try:
        img.save(buff, img_ext, icc_profile=img_icc)
    except OSError:
        # This usually happens when saving a JPEG with an ICC profile,
        # so we convert to RGB and try again
        img = img.convert('RGB')
        img.save(buff, img_ext, icc_profile=img_icc)
    except Exception as err:
        logging.error('Could not resize image %s, error: %s', file_name, err)
        abort(500)

    img.close()  # Close image to free memory, learned the hard way
    buff.seek(0)  # Reset buffer to start

    return send_file(buff, mimetype='image/' + img_ext)


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
    except Exception as err:
        logging.error('Could not save file: %s', err)
        abort(500)

    img_exif = mt.Metadata(img_path).yoink()  # Get EXIF data
    img_colors = ColorThief(img_path).get_palette(color_count=3) # Get color palette

    # Save to database
    try:
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
    except Exception as err:
        logging.error('Could not save to database: %s', err)
        abort(500)

    return 'Gwa Gwa' # Return something so the browser doesn't show an error


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
        if not db_session.query(db.GroupJunction)\
                         .filter_by(group_id=group_id, post_id=image_id)\
                         .first():
            db_session.add(db.GroupJunction(group_id=group_id,
                                            post_id=image_id,
                                            date_added=dt.utcnow()))
    elif request.form['action'] == 'remove':
        db_session.query(db.GroupJunction)\
                  .filter_by(group_id=group_id, post_id=image_id)\
                  .delete()

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


@blueprint.route('/logfile')
@login_required
def logfile():
    """
    Gets the log file and returns it as a JSON object
    """
    log_dict = {}

    with open('only.log', encoding='utf-8', mode='r') as file:
        for i, line in enumerate(file):
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

    return jsonify(log_dict)

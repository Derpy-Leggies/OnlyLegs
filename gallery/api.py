"""
Onlylegs - API endpoints
Used intermally by the frontend and possibly by other applications
"""
from uuid import uuid4
import os
import io
import logging

from flask import (
    Blueprint, current_app, send_from_directory, send_file, request, g, abort, flash, jsonify)
from werkzeug.utils import secure_filename

from PIL import Image, ImageOps # ImageFilter
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
    """
    # Get args
    width = request.args.get('w', default=0, type=int)  # Width of image
    height = request.args.get('h', default=0, type=int)  # Height of image
    filtered = request.args.get('f', default=False, type=bool)  # Whether to apply filters

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

    if not form_file:
        return abort(404)

    img_ext = os.path.splitext(form_file.filename)[-1].replace('.', '').lower()
    img_name = f"GWAGWA_{str(uuid4())}.{img_ext}"

    if not img_ext in current_app.config['ALLOWED_EXTENSIONS'].keys():
        logging.info('File extension not allowed: %s', img_ext)
        abort(403)

    if os.path.isdir(current_app.config['UPLOAD_FOLDER']) is False:
        os.mkdir(current_app.config['UPLOAD_FOLDER'])

    # Save to database
    try:
        db_session.add(db.posts(img_name, form['description'], form['alt'], g.user.id))
        db_session.commit()
    except Exception as err:
        logging.error('Could not save to database: %s', err)
        abort(500)

    # Save file
    try:
        form_file.save(
            os.path.join(current_app.config['UPLOAD_FOLDER'], img_name))
    except Exception as err:
        logging.error('Could not save file: %s', err)
        abort(500)

    return 'Gwa Gwa'


@blueprint.route('/remove/<int:img_id>', methods=['POST'])
@login_required
def remove(img_id):
    """
    Deletes an image from the server and database
    """
    img = db_session.query(db.posts).filter_by(id=img_id).first()

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
        db_session.query(db.posts).filter_by(id=img_id).delete()
        db_session.commit()
    except Exception as err:
        logging.error('Could not remove from database: %s', err)
        abort(500)

    logging.info('Removed image (%s) %s', img_id, img.file_name)
    flash(['Image was all in Le Head!', 1])
    return 'Gwa Gwa'


@blueprint.route('/metadata/<int:img_id>', methods=['GET'])
def metadata(img_id):
    """
    Yoinks metadata from an image
    """
    img = db_session.query(db.posts).filter_by(id=img_id).first()

    if img is None:
        abort(404)

    exif = mt.metadata.yoink(
        os.path.join(current_app.config['UPLOAD_FOLDER'], img.file_name))

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

from flask import Blueprint, current_app, send_from_directory, send_file, request, g, abort, flash, jsonify
from werkzeug.utils import secure_filename

from gallery.auth import login_required
from gallery.db import get_db

from PIL import Image, ImageOps
from . import metadata as mt

from .logger import logger

from uuid import uuid4
import io
import os
import time

blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/uploads/<file>/<int:quality>', methods=['GET'])
def uploads(file, quality):
    # If quality is 0, return original file
    if quality == 0:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                                   secure_filename(file),
                                   as_attachment=True)

    # Set variables
    set_ext = current_app.config['ALLOWED_EXTENSIONS']
    buff = io.BytesIO()

    # Open image and set extension
    try:
        img = Image.open(
            os.path.join(current_app.config['UPLOAD_FOLDER'],
                        secure_filename(file)))
    except Exception as e:
        logger.server(600, f"Error opening image: {e}")
        abort(500)
        
    img_ext = os.path.splitext(secure_filename(file))[-1].lower().replace(
        '.', '')
    img_ext = set_ext[img_ext]
    img_icc = img.info.get(
        "icc_profile")  # Get ICC profile as it alters colours

    # Resize image and orientate correctly
    img.thumbnail((quality, quality), Image.LANCZOS)
    img = ImageOps.exif_transpose(img)
    try:
        img.save(buff, img_ext, icc_profile=img_icc)
    except OSError:
        # This usually happens when saving a JPEG with an ICC profile
        # Convert to RGB and try again
        img = img.convert('RGB')
        img.save(buff, img_ext, icc_profile=img_icc)
    except:
        logger.server(600, f"Error resizing image: {file}")
        abort(500)
        
    img.close()

    # Seek to beginning of buffer and return
    buff.seek(0)
    return send_file(buff, mimetype='image/' + img_ext)


@blueprint.route('/upload', methods=['POST'])
@login_required
def upload():
    form_file = request.files['file']
    form = request.form

    if not form_file:
        return abort(404)

    img_ext = os.path.splitext(secure_filename(form_file.filename))[-1].replace('.', '').lower()
    img_name = f"GWAGWA_{uuid4().__str__()}.{img_ext}"

    if not img_ext in current_app.config['ALLOWED_EXTENSIONS'].keys():
        logger.add(303, f"File extension not allowed: {img_ext}")
        abort(403)
        
    if os.path.isdir(current_app.config['UPLOAD_FOLDER']) == False:
        os.mkdir(current_app.config['UPLOAD_FOLDER'])

    # Save to database
    try:
        db = get_db()
        db.execute(
            'INSERT INTO posts (file_name, author_id, description, alt)'
            ' VALUES (?, ?, ?, ?)',
            (img_name, g.user['id'], form['description'], form['alt']))
    except Exception as e:
        logger.server(600, f"Error saving to database: {e}")
        abort(500)
        
    # Save file
    try:
        form_file.save(
            os.path.join(current_app.config['UPLOAD_FOLDER'], img_name))
        db.commit()
    except Exception as e:
        logger.server(600, f"Error saving file: {e}")
        abort(500)

    return 'Gwa Gwa'


@blueprint.route('/remove/<int:id>', methods=['POST'])
@login_required
def remove(id):
    img = get_db().execute(
        'SELECT author_id, file_name FROM posts WHERE id = ?',
        (id, )).fetchone()

    if img is None:
        abort(404)
    if img['author_id'] != g.user['id']:
        abort(403)

    try:
        os.remove(
            os.path.join(current_app.config['UPLOAD_FOLDER'],
                         img['file_name']))
    except Exception as e:
        logger.server(600, f"Error removing file: {e}")
        abort(500)

    try:
        db = get_db()
        db.execute('DELETE FROM posts WHERE id = ?', (id, ))
        db.commit()
    except:
        logger.server(600, f"Error removing from database: {e}")
        abort(500)

    logger.server(301, f"Removed image {id}")
    flash(['Image was all in Le Head!', 1])
    return 'Gwa Gwa'


@blueprint.route('/metadata/<int:id>', methods=['GET'])
def metadata(id):
    img = get_db().execute(
        'SELECT file_name, description, alt FROM posts WHERE id = ?',
        (id, )).fetchone()

    if img is None:
        abort(404)

    exif = mt.metadata.yoink(
        os.path.join(current_app.config['UPLOAD_FOLDER'], img['file_name']))

    return jsonify(exif)

@blueprint.route('/logfile')
@login_required
def logfile():
    filename = logger.filename()
    log_dict = {}
    i = 0
    
    with open(filename) as f:
        for line in f:
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
            except:
                message_data = {
                    'code': 0,
                    'message': message
                }
                
            log_dict[i] = {
                'event': event_data,
                'message': message_data
            }
                            
            i += 1 # Line number, starts at 0
        
    return jsonify(log_dict)
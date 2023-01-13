from flask import Blueprint, render_template, current_app, send_from_directory, send_file, request, g, abort, flash
from werkzeug.utils import secure_filename
from gallery.auth import login_required
from gallery.db import get_db
from PIL import Image, ImageOps
import io
import os
from uuid import uuid4

blueprint = Blueprint('viewsbp', __name__, url_prefix='/api')


@blueprint.route('/uploads/<file>/<int:quality>', methods=['GET'])
def uploads(file, quality):
    # If quality is 0, return original file
    if quality == 0:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], secure_filename(file), as_attachment=True)

    # Set variables
    set_ext = {'jpg': 'jpeg', 'jpeg': 'jpeg', 'png': 'png', 'webp': 'webp'}
    buff = io.BytesIO()
    
    # Open image and set extension
    img = Image.open(os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(file)))
    img_ext = os.path.splitext(secure_filename(file))[-1].lower().replace('.', '')
    img_ext = set_ext[img_ext]
    
    # Resize image and orientate correctly
    img.thumbnail((quality, quality), Image.LANCZOS)
    img = ImageOps.exif_transpose(img)
    img.save(buff, img_ext)

    # Seek to beginning of buffer and return
    buff.seek(0)
    return send_file(buff, mimetype='image/'+img_ext)

@blueprint.route('/upload', methods=['POST'])
@login_required
def upload():
    form_file = request.files['file']
    form = request.form

    if not form_file:
        return abort(404)
    
    img_ext = os.path.splitext(secure_filename(form_file.filename))[-1].lower()
    img_name = f"GWAGWA_{uuid4().__str__()}{img_ext}"

    if not img_ext in current_app.config['ALLOWED_EXTENSIONS']:
        return 'File extension not allowed: '+img_ext
    
    # Save to database
    try:
        db = get_db()
        db.execute(
            'INSERT INTO posts (file_name, author_id, description, alt)'
            ' VALUES (?, ?, ?, ?)',
            (img_name, g.user['id'], form['description'], form['alt'])
        )
        db.commit()
    except Exception as e:
        abort(500)
    
    # Save file  
    try:
        form_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], img_name))
    except:
        abort(500)
    
    return 'Gwa Gwa'

@blueprint.route('/remove/<int:id>', methods=['POST'])
@login_required
def remove(id):
    img = get_db().execute(
        'SELECT author_id, file_name FROM posts WHERE id = ?',
        (id,)
    ).fetchone()

    if img is None:
        abort(404)
    if img['author_id'] != g.user['id']:
        abort(403)
    
    try:
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], img['file_name']))
    except Exception as e:
        abort(500)
    
    try:
        db = get_db()
        db.execute('DELETE FROM posts WHERE id = ?', (id,))
        db.commit()
    except:
        abort(500)
    
    return 'Gwa Gwa'
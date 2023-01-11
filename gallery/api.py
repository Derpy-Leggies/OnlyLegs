from flask import Blueprint, render_template, current_app, send_from_directory, request, g, abort, flash
from werkzeug.utils import secure_filename
from gallery.auth import login_required
from gallery.db import get_db
from PIL import Image
import os
from uuid import uuid4

blueprint = Blueprint('viewsbp', __name__, url_prefix='/api')


@blueprint.route('/uploads/<quality>/<file>')
def uploads(quality, file):
    dir = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(quality))
    file = secure_filename(file)

    return send_from_directory(dir, file, as_attachment=True)

@blueprint.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files['file']
    form = request.form
    
    # Check if file has been submitted
    if not file:
        flash('No selected file')
        return abort(404)
    
    # New file name and check if file extension is allowed
    file_ext = os.path.splitext(file.filename)[1].lower()
    file_name = f"GWAGWA_{uuid4().__str__()}{file_ext}"

    if not file_ext in current_app.config['ALLOWED_EXTENSIONS']:
        return 'File extension not allowed: '+file_ext
    
    try:
        file.save(os.path.join(current_app.instance_path, current_app.config['UPLOAD_FOLDER']+'/original', file_name))
    except:
        return 'Could not save file'

    # Resize image
    thumbnail_size = 300, 300
    preview_size = 1000, 1000
    img_file = Image.open(os.path.join(current_app.instance_path, current_app.config['UPLOAD_FOLDER']+'/original', file_name))
    
    try:
        # save thumbnail
        img_file.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
        img_file.save(os.path.join(current_app.instance_path, current_app.config['UPLOAD_FOLDER']+'/thumbnail', file_name))
        
        # save preview
        img_file.thumbnail(preview_size, Image.Resampling.LANCZOS)
        img_file.save(os.path.join(current_app.instance_path, current_app.config['UPLOAD_FOLDER']+'/preview', file_name))
    except Exception as e:
        return 'Could not resize image: '+ str(e)
    
    db = get_db()
    db.execute(
        'INSERT INTO posts (file_name, author_id, description, alt)'
        ' VALUES (?, ?, ?, ?)',
        (file_name, g.user['id'], form['description'], form['alt'])
    )
    db.commit()
    
    return 'Gwa Gwa'

@blueprint.route('/remove/<int:id>', methods=['POST'])
@login_required
def remove(id):
    image = get_db().execute(
        'SELECT author_id, file_name FROM posts WHERE id = ?',
        (id,)
    ).fetchone()

    if image is None:
        abort(404)
    if image['author_id'] != g.user['id']:
        abort(403)
    
    try:
        os.remove(os.path.join(current_app.instance_path, current_app.config['UPLOAD_FOLDER'], 'original', image['file_name']))
        os.remove(os.path.join(current_app.instance_path, current_app.config['UPLOAD_FOLDER'], 'thumbnail', image['file_name']))
        os.remove(os.path.join(current_app.instance_path, current_app.config['UPLOAD_FOLDER'], 'preview', image['file_name']))
    except Exception as e:
        return 'file error: '+str(e)
    
    try:
        db = get_db()
        db.execute('DELETE FROM posts WHERE id = ?', (id,))
        db.commit()
    except:
        return 'database error'
    
    return 'Gwa Gwa'
from flask import Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, current_app
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from gallery.db import get_db
import os
import datetime
from PIL import Image
from PIL.ExifTags import TAGS
dt = datetime.datetime.now()

blueprint = Blueprint('image', __name__, url_prefix='/image')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.author_id FROM posts p JOIN users u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        return False

    if check_author and post['author_id'] != g.user['id']:
        return False

    return post


@blueprint.route('/<int:id>', methods=('GET', 'POST'))
def image(id):
    if request.method == 'POST':
        image = get_post(id)
        action = request.form['action']
        
        if not image:
            abort(403)
        
        if action == 'delete':
            try:
                db = get_db()
                db.execute('DELETE FROM posts WHERE id = ?', (id,))
                db.commit()
            except:
                return 'database error'
                
            try:
                os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], 'original', image['file_name']))
            except:
                return 'os error'
    
    # GET, it should be called Gwa Gwa because it sounds funny
    # Get image from database
    db = get_db()
    image = db.execute(
        'SELECT * FROM posts'
        ' WHERE id = ?',
        (id,)
    ).fetchone()
    
    if image is None:
        abort(404)
    
    # Get exif data from image
    try:
        file = Image.open(os.path.join(current_app.config['UPLOAD_FOLDER'], 'original', image['file_name']))
        raw_exif = file.getexif()
        human_exif = {}
        
        for tag in raw_exif:
            name = TAGS.get(tag, tag)
            value = raw_exif.get(tag)
            
            if isinstance(value, bytes):
                value = value.decode()
            
            human_exif[name] = value
        
        if len(human_exif) == 0:
            human_exif = False
    except:
        # Cringe, no file present
        human_exif = False
    
    # All in le head    
    return render_template('image.html', image=image, exif=human_exif, file=file)
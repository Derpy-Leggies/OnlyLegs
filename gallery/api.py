import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, jsonify, send_from_directory
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from gallery.db import get_db

blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/uploads/<quality>/<request_file>', methods=['POST'])
def uploads(quality, request_file):
    if request.method != 'POST':
        abort(405)

    #quality = secure_filename(quality)
    #quality_dir = os.path.join(app.config['UPLOAD_FOLDER'], quality)
    #if not os.path.isdir(quality_dir):
    #    abort(404)

    #request_file = secure_filename(request_file)

    #if not os.path.isfile(os.path.join(quality_dir, request_file)):
    #    abort(404)

    #return send_from_directory(quality_dir, request_file)
    abort(404)
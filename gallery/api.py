from flask import Blueprint, render_template, current_app, send_from_directory
from werkzeug.utils import secure_filename
import os

blueprint = Blueprint('viewsbp', __name__, url_prefix='/')


@blueprint.route('/uploads/<quality>/<file>')
def uploads(quality, file):
    dir = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(quality))
    file = secure_filename(file)

    return send_from_directory(dir, file, as_attachment=True)
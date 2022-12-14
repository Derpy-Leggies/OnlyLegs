from flask import Flask, render_template, send_from_directory, abort, url_for, jsonify, redirect, request, session
from werkzeug.utils import secure_filename
import os

# Get database stuff
DB_USER = os.environ.get('USERNAME')
DB_PASS = os.environ.get('PASSWORD')
DB_HOST = os.environ.get('HOST')
DB_PORT = os.environ.get('PORT')

DB = os.environ.get('DATABASE')

# Set flask config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#
#   ERROR HANDLERS
#
@app.errorhandler(405)
def method_not_allowed(e):
    error = '405'
    msg = 'Method sussy wussy'
    return render_template('error.html', error=error, msg=msg), 404


@app.errorhandler(404)
def page_not_found(e):
    error = '404'
    msg = 'Could not find what you need!'
    return render_template('error.html', error=error, msg=msg), 404


@app.errorhandler(403)
def forbidden(e):
    error = '403'
    msg = 'Go away! This is no place for you!'
    return render_template('error.html', error=error, msg=msg), 403


@app.errorhandler(410)
def gone(e):
    error = '410'
    msg = 'The page is no longer available! *sad face*'
    return render_template('error.html', error=error, msg=msg), 410


@app.errorhandler(500)
def internal_server_error(e):
    error = '500'
    msg = 'Server died inside :c'
    return render_template('error.html', error=error, msg=msg), 500


#
#   ROUTES
#
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/image/<file_id>')
def image(file_id):
    try:
        file_id = int(file_id)
    except ValueError:
        abort(404)

    file_list = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], 'original'))
    file_name = file_list[file_id]

    return render_template('image.html', fileName=file_name, id=file_id)


#
#   METHODS
#
@app.route('/fileList/<item_type>', methods=['GET'])
def image_list(item_type):
    if request.method != 'GET':
        abort(405)

    item_type = secure_filename(item_type)
    type_dir = os.path.join(app.config['UPLOAD_FOLDER'], item_type)
    if not os.path.isdir(type_dir):
        abort(404)

    return jsonify(os.listdir(type_dir))


@app.route('/uploads/<item_type>/<file_id>', methods=['GET'])
def uploads(item_type, file_id):
    if request.method != 'GET':
        abort(405)

    item_type = secure_filename(item_type)
    type_dir = os.path.join(app.config['UPLOAD_FOLDER'], item_type)
    if not os.path.isdir(type_dir):
        abort(404)

    file_id = secure_filename(file_id)
    if not os.path.isfile(os.path.join(type_dir, file_id)):
        abort(404)

    return send_from_directory(type_dir, file_id)

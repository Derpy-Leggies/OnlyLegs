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
IMAGE_DIR = os.path.join(BASE_DIR, 'static/images')

app = Flask(__name__)
app.config['IMAGE_DIR'] = IMAGE_DIR


#
#   ERROR HANDLERS
#
@app.errorhandler(405)
def method_not_allowed(e):
    error = '405'
    msg = 'Method sussy wussy'
    return render_template('error.html', error = error, msg = msg), 404

@app.errorhandler(404)
def page_not_found(e):
    error = '404'
    msg = 'Could not find what you need!'
    return render_template('error.html', error = error, msg = msg), 404

@app.errorhandler(403)
def forbidden(e):
    error = '403'
    msg = 'Go away! This is no place for you!'
    return render_template('error.html', error = error, msg = msg), 403

@app.errorhandler(410)
def gone(e):
    error = '410'
    msg = 'The page is no longer available! *sad face*'
    return render_template('error.html', error = error, msg = msg), 410

@app.errorhandler(500)
def internal_server_error(e):
    error = '500'
    msg = 'Server died inside :c'
    return render_template('error.html', error = error, msg = msg), 500


#
#   ROUTES
#
@app.route('/')
def home():
    image_list = os.listdir(app.config['IMAGE_DIR'])
    return render_template('home.html', images = image_list)

@app.route('/image/<id>')
def image(id):
    try:
        id = int(id)
    except ValueError:
        abort(404)
        
    image_list = os.listdir(app.config['IMAGE_DIR'])
    fileName = image_list[id]
        
    return render_template('image.html', fileName = fileName, id = id)


#
#   METHODS
#
@app.route('/fileList', methods = ['GET'])
def imageList():
    image_list = os.listdir(app.config['IMAGE_DIR'])
    return jsonify(image_list)

@app.route('/file/<filename>', methods = ['GET'])
def pfp(filename):
    if (request.method == 'GET'):
        return send_from_directory(app.config['IMAGE_DIR'], filename)
    else:
        return None
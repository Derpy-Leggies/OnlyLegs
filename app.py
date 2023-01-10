print("""
  ___        _       _
 / _ \\ _ __ | |_   _| |    ___  __ _ ___
| | | | '_ \\| | | | | |   / _ \\/ _` / __|
| |_| | | | | | |_| | |__|  __/ (_| \\__ \\
 \\___/|_| |_|_|\\__, |_____\\___|\\__, |___/
               |___/           |___/
Created by Fluffy Bean  -  Version 100123
""")

# Import base packages
import time
import sys
import os

# Import required OnlyLegs packages
from packages import onlylegsDB
onlylegsDB = onlylegsDB.DBmanager()
onlylegsDB.initialize()

from packages import onlylegsSass
onlylegsSass = onlylegsSass.Sassy('default')

# Import flask
from flask import Flask, render_template, send_from_directory, abort, url_for, jsonify, redirect, request, session
from werkzeug.utils import secure_filename

# Set flask config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'usr', 'uploads')

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

@app.route('/group')
def group():
    return render_template('group.html', group_id='gwa gwa')

@app.route('/group/<group_id>')
def group_id(group_id):
    try:
        group_id = int(group_id)
    except ValueError:
        abort(404)
    
    return render_template('group.html', group_id=group_id)

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/upload/form', methods=['POST'])
def upload_form():
    if request.method != 'POST':
        abort(405)

    return 'balls'

@app.route('/profile')
def profile():
    return render_template('profile.html', user_id='gwa gwa')

@app.route('/profile/<user_id>')
def profile_id(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        abort(404)
        
    return render_template('profile.html', user_id=user_id)

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/image/<request_id>')
def image(request_id):
    # Check if request_id is valid
    try:
        request_id = int(request_id)
    except ValueError:
        abort(404)
    
    result = onlylegsDB.getImage(request_id)
    
    return render_template('image.html', fileName=result[1], id=request_id)


#
#   METHODS
#
@app.route('/fileList/<item_type>', methods=['GET'])
def image_list(item_type):
    if request.method != 'GET':
        abort(405)
    
    cursor = onlylegsDB.database.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY id DESC")
    
    item_list = cursor.fetchall()

    return jsonify(item_list)

@app.route('/uploads/<quality>/<request_file>', methods=['GET'])
def uploads(quality, request_file):
    if request.method != 'GET':
        abort(405)

    quality = secure_filename(quality)
    quality_dir = os.path.join(app.config['UPLOAD_FOLDER'], quality)
    if not os.path.isdir(quality_dir):
        abort(404)

    request_file = secure_filename(request_file)

    if not os.path.isfile(os.path.join(quality_dir, request_file)):
        abort(404)

    return send_from_directory(quality_dir, request_file)

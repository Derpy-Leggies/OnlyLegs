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
#from packages import onlylegsDB
#onlylegsDB = onlylegsDB.DBmanager()
#onlylegsDB.initialize()

#from packages import onlylegsSass
#onlylegsSass = onlylegsSass.Sassy('default')

# Import flask
from flask import *
from werkzeug.utils import secure_filename

def create_app(test_config=None):
    from dotenv import load_dotenv
    load_dotenv(os.path.join('./gallery', 'user', '.env'))
    
    # create and configure the app
    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('FLASK_SECRET'),
        DATABASE=os.path.join(app.instance_path, 'gallery.sqlite'),
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

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
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import routes
    app.register_blueprint(routes.bp)
    app.add_url_rule('/', endpoint='index')


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

    from . import db
    db.init_app(app)

    return app
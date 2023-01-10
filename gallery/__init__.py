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

# Import flask
from flask import *
from werkzeug.utils import secure_filename

def create_app(test_config=None):
    # Get environment variables
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
    
    
    # Load database
    from . import db
    db.init_app(app)
    
    # Load theme
    #from . import sassy
    #sassy.compile('default')


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
    
    
    # Load login, registration and logout manager
    from . import auth
    app.register_blueprint(auth.blueprint)
    
    # Load apis
    from . import api
    app.register_blueprint(api.blueprint)
    
    # Load routes for home and images
    from . import gallery
    app.register_blueprint(gallery.blueprint)
    app.add_url_rule('/', endpoint='index')


    return app
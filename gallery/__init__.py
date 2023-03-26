"""
Onlylegs Gallery
This is the main app file, it loads all the other files and sets up the app
"""

# Import system modules
import os
import logging

# Flask
from flask_compress import Compress
from flask_caching import Cache
from flask_assets import Environment, Bundle
from flask import Flask, render_template, abort
from werkzeug.exceptions import HTTPException

# Configuration
import platformdirs
from dotenv import load_dotenv
from yaml import safe_load

# Utils
from gallery.utils import theme_manager


USER_DIR = platformdirs.user_config_dir('onlylegs')


def create_app(test_config=None):
    """
    Create and configure the main app
    """
    app = Flask(__name__, instance_path=os.path.join(USER_DIR, 'instance'))
    assets = Environment()
    cache = Cache(config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})
    compress = Compress()

    # Get environment variables
    load_dotenv(os.path.join(USER_DIR, '.env'))
    print("Loaded environment variables")

    # Get config file
    with open(os.path.join(USER_DIR, 'conf.yml'), encoding='utf-8') as file:
        conf = safe_load(file)
        print("Loaded gallery config")

    # App configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('FLASK_SECRET'),
        DATABASE=os.path.join(app.instance_path, 'gallery.sqlite'),
        UPLOAD_FOLDER=os.path.join(USER_DIR, 'uploads'),
        ALLOWED_EXTENSIONS=conf['upload']['allowed-extensions'],
        MAX_CONTENT_LENGTH=1024 * 1024 * conf['upload']['max-size'],
        WEBSITE=conf['website'],
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Load theme
    theme_manager.CompileTheme('default', app.root_path)

    # Bundle JS files
    js_scripts = Bundle('js/*.js', output='gen/packed.js')
    assets.register('js_all', js_scripts)

    # Error handlers
    @app.errorhandler(Exception)
    def error_page(err):
        # If the error is a HTTP error, return the error page
        if isinstance(err, HTTPException):
            error = err.code
            msg = err.description
            return render_template('error.html', error=error, msg=msg), err.code

        # Otherwise this an internal error
        abort(500)

    # Load login, registration and logout manager
    from gallery import auth
    app.register_blueprint(auth.blueprint)

    # Load the different routes
    from .routes import api, groups, routing, settings
    app.register_blueprint(api.blueprint)
    app.register_blueprint(groups.blueprint)
    app.register_blueprint(routing.blueprint)
    app.register_blueprint(settings.blueprint)

    # Log to file that the app has started
    logging.info('Gallery started successfully!')

    # Initialize extensions and return app
    assets.init_app(app)
    cache.init_app(app)
    compress.init_app(app)
    return app

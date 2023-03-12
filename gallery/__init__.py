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
from flask import Flask, render_template

# Configuration
from dotenv import load_dotenv
import platformdirs
from yaml import FullLoader, load


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
    with open(os.path.join(USER_DIR, 'conf.yml'), encoding='utf-8') as f:
        conf = load(f, Loader=FullLoader)
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

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Load theme
    from . import theme_manager
    theme_manager.CompileTheme('default', app.root_path)
    
    # Bundle JS files
    js = Bundle('js/*.js', output='gen/packed.js')
    assets.register('js_all', js)

    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(405)
    @app.errorhandler(410)
    @app.errorhandler(500)
    def error_page(err):
        error = err.code
        msg = err.description
        return render_template('error.html', error=error, msg=msg), err.code

    # Load login, registration and logout manager
    from . import auth
    app.register_blueprint(auth.blueprint)

    # Load routes for home and images
    from . import routing
    app.register_blueprint(routing.blueprint)
    app.add_url_rule('/', endpoint='index')
    
    # Load routes for groups
    from . import groups
    app.register_blueprint(groups.blueprint)

    # Load routes for settings
    from . import settings
    app.register_blueprint(settings.blueprint)

    # Load APIs
    from . import api
    app.register_blueprint(api.blueprint)

    logging.info('Gallery started successfully!')

    assets.init_app(app)
    cache.init_app(app)
    compress.init_app(app)
    return app

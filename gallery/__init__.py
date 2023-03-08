"""
  ___        _       _
 / _ \ _ __ | |_   _| |    ___  __ _ ___
| | | | '_ \| | | | | |   / _ \/ _` / __|
| |_| | | | | | |_| | |__|  __/ (_| \__ \ 
 \___/|_| |_|_|\__, |_____\___|\__, |___/
               |___/           |___/
Created by Fluffy Bean - Version 23.03.04
"""

# Import system modules
import os
import sys
import logging

# Flask
from flask_compress import Compress
from flask_caching import Cache
from flask import Flask, render_template

# Configuration
from dotenv import load_dotenv
import platformdirs
import yaml

from . import theme_manager


USER_DIR = platformdirs.user_config_dir('onlylegs')
INSTANCE_PATH = os.path.join(USER_DIR, 'instance')


# Check if any of the required files are missing
if not os.path.exists(platformdirs.user_config_dir('onlylegs')):
    from . import setup
    setup.SetupApp()

# Get environment variables
if os.path.exists(os.path.join(USER_DIR, '.env')):
    load_dotenv(os.path.join(USER_DIR, '.env'))
    print("Loaded environment variables")
else:
    print("No environment variables found!")
    sys.exit(1)


# Get config file
if os.path.exists(os.path.join(USER_DIR, 'conf.yml')):
    with open(os.path.join(USER_DIR, 'conf.yml'), encoding='utf-8') as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
        print("Loaded gallery config")
else:
    print("No config file found!")
    sys.exit(1)

# Setup the logging config
LOGS_PATH = os.path.join(platformdirs.user_config_dir('onlylegs'), 'logs')

if not os.path.isdir(LOGS_PATH):
    os.mkdir(LOGS_PATH)

logging.getLogger('werkzeug').disabled = True
logging.basicConfig(
    filename=os.path.join(LOGS_PATH, 'only.log'),
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
    encoding='utf-8')


def create_app(test_config=None):
    """
    Create and configure the main app
    """
    app = Flask(__name__,instance_path=INSTANCE_PATH)
    compress = Compress()
    cache = Cache(config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 69})

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


    theme_manager.CompileTheme('default', app.root_path)


    @app.errorhandler(405)
    def method_not_allowed(err):
        error = '405'
        msg = err.description
        return render_template('error.html', error=error, msg=msg), 404

    @app.errorhandler(404)
    def page_not_found(err):
        error = '404'
        msg = err.description
        return render_template('error.html', error=error, msg=msg), 404

    @app.errorhandler(403)
    def forbidden(err):
        error = '403'
        msg = err.description
        return render_template('error.html', error=error, msg=msg), 403

    @app.errorhandler(410)
    def gone(err):
        error = '410'
        msg = err.description
        return render_template('error.html', error=error, msg=msg), 410

    @app.errorhandler(500)
    def internal_server_error(err):
        error = '500'
        msg = err.description
        return render_template('error.html', error=error, msg=msg), 500

    # Load login, registration and logout manager
    from . import auth
    app.register_blueprint(auth.blueprint)

    # Load routes for home and images
    from . import routing
    app.register_blueprint(routing.blueprint)
    app.add_url_rule('/', endpoint='index')

    # Load routes for settings
    from . import settings
    app.register_blueprint(settings.blueprint)

    # Load APIs
    from . import api
    app.register_blueprint(api.blueprint)

    compress.init_app(app)
    cache.init_app(app)
    return app

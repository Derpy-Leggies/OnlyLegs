print("""
  ___        _       _
 / _ \\ _ __ | |_   _| |    ___  __ _ ___
| | | | '_ \\| | | | | |   / _ \\/ _` / __|
| |_| | | | | | |_| | |__|  __/ (_| \\__ \\
 \\___/|_| |_|_|\\__, |_____\\___|\\__, |___/
               |___/           |___/
Created by Fluffy Bean - Version 23.03.02
""")

from flask import Flask, render_template
from flask_compress import Compress

from dotenv import load_dotenv
import platformdirs

import yaml
import os

# I could use something other than the config dir, but this works well enough
user_dir = platformdirs.user_config_dir('onlylegs')
if not os.path.exists(user_dir):
    os.makedirs(user_dir)
    print("Created user directory")
# Location of instance folder, where sqlite db is stored
instance_path = os.path.join(user_dir, 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)
    print("Created instance directory")

# Get environment variables
if os.path.exists(os.path.join(user_dir, '.env')):
    load_dotenv(os.path.join(user_dir, '.env'))
    print("Loaded environment variables")
else:
    conf = {
        'FLASK_SECRETE': 'dev',
    }
    # Create .env file with default values
    with open(os.path.join(user_dir, '.env'), 'w') as f:
        for key, value in conf.items():
            f.write(f"{key}={value}\n")
        print("Created default environment variables at:",
              os.path.join(user_dir, '.env'),
              "\nCHANGE THESE VALUES USING TEHE GALLERY!")

# Get config file
if os.path.exists(os.path.join(user_dir, 'conf.yml')):
    with open(os.path.join(user_dir, 'conf.yml'), 'r') as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
        print("Loaded gallery config")
else:
    conf = {
        'admin': {
            'name': 'Real Person',
            'username': 'User',
            'email': 'real-email@some.place'
        },
        'upload': {
            'allowed-extensions': {
                'jpg': 'jpeg',
                'jpeg': 'jpeg',
                'png': 'png',
                'webp': 'webp'
            },
            'max-size': 69,
            'rename': 'GWA_\{\{username\}\}_\{\{time\}\}'
        },
        'website': {
            'name': 'OnlyLegs',
            'motto': 'Gwa Gwa',
            'language': 'english'
        }
    }
    # Create yaml config file with default values
    with open(os.path.join(user_dir, 'conf.yml'), 'w') as f:
        yaml.dump(conf, f, default_flow_style=False)
        print("Created default gallery config at:",
              os.path.join(user_dir, 'conf.yml'),
              "\nCHANGE THESE VALUES USING TEHE GALLERY!")

# Load logger
from .logger import logger

logger.innit_logger()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_path=instance_path)
    compress = Compress()

    # App configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('FLASK_SECRET'),
        DATABASE=os.path.join(app.instance_path, 'gallery.sqlite'),
        UPLOAD_FOLDER=os.path.join(user_dir, 'uploads'),
        MAX_CONTENT_LENGTH=1024 * 1024 * conf['upload']['max-size'],
        ALLOWED_EXTENSIONS=conf['upload']['allowed-extensions'],
        WEBSITE=conf['website'],
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
    from . import sassy
    sassy.compile('default', app.root_path)

    @app.errorhandler(405)
    def method_not_allowed(e):
        error = '405'
        msg = e.description
        return render_template('error.html', error=error, msg=e), 404

    @app.errorhandler(404)
    def page_not_found(e):
        error = '404'
        msg = e.description
        return render_template('error.html', error=error, msg=msg), 404

    @app.errorhandler(403)
    def forbidden(e):
        error = '403'
        msg = e.description
        return render_template('error.html', error=error, msg=msg), 403

    @app.errorhandler(410)
    def gone(e):
        error = '410'
        msg = e.description
        return render_template('error.html', error=error, msg=msg), 410

    @app.errorhandler(500)
    def internal_server_error(e):
        error = '500'
        msg = e.description
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
    return app
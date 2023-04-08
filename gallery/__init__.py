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
from flask_login import LoginManager
from flask import Flask, render_template, abort
from werkzeug.exceptions import HTTPException

# Configuration
import platformdirs
from dotenv import load_dotenv
from yaml import safe_load

# Import database
from sqlalchemy.orm import sessionmaker
from gallery import db


USER_DIR = platformdirs.user_config_dir("onlylegs")


db_session = sessionmaker(bind=db.engine)
db_session = db_session()
login_manager = LoginManager()
assets = Environment()
cache = Cache(config={"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 300})
compress = Compress()


def create_app(test_config=None):
    """
    Create and configure the main app
    """
    app = Flask(__name__, instance_path=os.path.join(USER_DIR, "instance"))

    # Get environment variables
    load_dotenv(os.path.join(USER_DIR, ".env"))
    print("Loaded environment variables")

    # Get config file
    with open(os.path.join(USER_DIR, "conf.yml"), encoding="utf-8", mode="r") as file:
        conf = safe_load(file)
        print("Loaded config")

    # App configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("FLASK_SECRET"),
        DATABASE=os.path.join(app.instance_path, "gallery.sqlite3"),
        UPLOAD_FOLDER=os.path.join(USER_DIR, "uploads"),
        ALLOWED_EXTENSIONS=conf["upload"]["allowed-extensions"],
        MAX_CONTENT_LENGTH=1024 * 1024 * conf["upload"]["max-size"],
        ADMIN_CONF=conf["admin"],
        UPLOAD_CONF=conf["upload"],
        WEBSITE_CONF=conf["website"],
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    login_manager.init_app(app)
    login_manager.login_view = "gallery.index"
    login_manager.session_protection = "strong"

    @login_manager.user_loader
    def load_user(user_id):
        return db_session.query(db.Users).filter_by(alt_id=user_id).first()

    @login_manager.unauthorized_handler
    def unauthorized():
        error = 401
        msg = "You are not authorized to view this page!!!!"
        return render_template("error.html", error=error, msg=msg), error

    lib = Bundle(
        "lib/*.js", filters="jsmin", output="gen/lib.js", depends="lib/*.js"
    )
    js = Bundle(
        "js/*.js", filters="jsmin", output="gen/index.js", depends="js/*.js"
    )
    styles = Bundle(
        "sass/*.sass", filters="libsass,cssmin", output="gen/styles.css", depends='sass/**/*.sass'
    )

    assets.register("lib", lib)
    assets.register("js", js)
    assets.register("styles", styles)

    # Error handlers, if the error is not a HTTP error, return 500
    @app.errorhandler(Exception)
    def error_page(err):  # noqa
        if not isinstance(err, HTTPException):
            abort(500)
        return (
            render_template("error.html", error=err.code, msg=err.description),
            err.code,
        )

    # Load login, registration and logout manager
    from gallery import auth

    app.register_blueprint(auth.blueprint)

    # Load the API
    from gallery import api

    app.register_blueprint(api.blueprint)

    # Load the different views
    from gallery.views import index, image, group, settings, profile

    app.register_blueprint(index.blueprint)
    app.register_blueprint(image.blueprint)
    app.register_blueprint(group.blueprint)
    app.register_blueprint(profile.blueprint)
    app.register_blueprint(settings.blueprint)

    # Log to file that the app has started
    logging.info("Gallery started successfully!")

    # Initialize extensions and return app
    assets.init_app(app)
    cache.init_app(app)
    compress.init_app(app)
    return app

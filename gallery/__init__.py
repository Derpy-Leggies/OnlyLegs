"""
Onlylegs Gallery
This is the main app file, it loads all the other files and sets up the app
"""
# Import system modules
import os
import logging

# Flask
from flask_assets import Bundle
from flask import Flask, render_template, abort
from werkzeug.exceptions import HTTPException

from gallery.extensions import db, migrate, login_manager, assets, compress, cache
from gallery.models import Users
from gallery.views import index, image, group, settings, profile
from gallery import api
from gallery import auth

# Configuration
import platformdirs


INSTACE_DIR = os.path.join(platformdirs.user_config_dir("onlylegs"),
                           "instance")


def create_app():  # pylint: disable=R0914
    """
    Create and configure the main app
    """
    app = Flask(__name__, instance_path=INSTACE_DIR)
    app.config.from_pyfile("config.py")

    db.init_app(app)
    migrate.init_app(app, db)

    # if database file doesn't exist, create it
    if not os.path.exists(os.path.join(INSTACE_DIR, "gallery.sqlite3")):
        print("Creating database")
        with app.app_context():
            db.create_all()

    login_manager.init_app(app)
    login_manager.login_view = "gallery.index"
    login_manager.session_protection = "normal"

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.filter_by(alt_id=user_id).first()

    @login_manager.unauthorized_handler
    def unauthorized():
        error = 401
        msg = "You are not authorized to view this page!!!!"
        return render_template("error.html", error=error, msg=msg), error

    # Error handlers, if the error is not a HTTP error, return 500
    @app.errorhandler(Exception)
    def error_page(err):  # noqa
        if not isinstance(err, HTTPException):
            abort(500)
        return (
            render_template("error.html", error=err.code, msg=err.description),
            err.code,
        )

    scripts = Bundle("js/*.js", filters="jsmin", output="gen/js.js", depends="js/*.js")

    styles = Bundle(
        "sass/*.sass",
        filters="libsass, cssmin",
        output="gen/styles.css",
        depends="sass/**/*.sass",
    )

    assets.register("scripts", scripts)
    assets.register("styles", styles)

    # Load all the blueprints
    app.register_blueprint(auth.blueprint)
    app.register_blueprint(api.blueprint)
    app.register_blueprint(index.blueprint)
    app.register_blueprint(image.blueprint)
    app.register_blueprint(group.blueprint)
    app.register_blueprint(profile.blueprint)
    app.register_blueprint(settings.blueprint)

    assets.init_app(app)
    cache.init_app(app)
    compress.init_app(app)

    print("Done!")
    logging.info("Gallery started successfully!")
    return app

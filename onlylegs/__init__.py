"""
Onlylegs Gallery
This is the main app file, it loads all the other files and sets up the app
"""
import os
import logging

from flask_assets import Bundle
from flask_migrate import init as migrate_init

from flask import Flask, render_template, abort
from werkzeug.exceptions import HTTPException
from werkzeug.security import generate_password_hash

from onlylegs.extensions import db, migrate, login_manager, assets, compress, cache
from onlylegs.config import INSTANCE_DIR, MIGRATIONS_DIR
from onlylegs.models import User
from onlylegs.views import (
    index as view_index,
    image as view_image,
    group as view_group,
    settings as view_settings,
    profile as view_profile,
)
from onlylegs.api import media as api_media, group as api_group, account as api_account
from onlylegs import auth as view_auth
from onlylegs import filters
from onlylegs import gwagwa


def create_app():  # pylint: disable=R0914
    """
    Create and configure the main app
    """
    app = Flask(__name__, instance_path=INSTANCE_DIR)
    app.config.from_pyfile("config.py")

    # DATABASE
    db.init_app(app)
    migrate.init_app(app, db, directory=MIGRATIONS_DIR)

    # If database file doesn't exist, create it
    if not os.path.exists(os.path.join(INSTANCE_DIR, "gallery.sqlite3")):
        print("Creating database")
        with app.app_context():
            db.create_all()

            register_user = User(
                username=app.config["ADMIN_CONF"]["username"],
                email=app.config["ADMIN_CONF"]["email"],
                password=generate_password_hash("changeme!", method="sha256"),
            )
            db.session.add(register_user)
            db.session.commit()

            print(
                """
####################################################
# DEFAULY ADMIN USER GENERATED WITH GIVEN USERNAME #
# THE DEFAULT PASSWORD "changeme!" HAS BEEN USED,  #
# PLEASE UPDATE IT IN THE SETTINGS!                #
####################################################
            """
            )

    # Check if migrations directory exists, if not create it
    with app.app_context():
        if not os.path.exists(MIGRATIONS_DIR):
            print("Creating migrations directory")
            migrate_init(directory=MIGRATIONS_DIR)

    # LOGIN MANAGER
    # can also set session_protection to "strong"
    # this would protect against session hijacking
    login_manager.init_app(app)
    login_manager.login_view = "onlylegs.index"

    @login_manager.user_loader
    def load_user(user_id):  # skipcq: PTC-W0065
        return User.query.filter_by(alt_id=user_id).first()

    @login_manager.unauthorized_handler
    def unauthorized():  # skipcq: PTC-W0065
        error = 401
        msg = "You are not authorized to view this page!!!!"
        return render_template("error.html", error=error, msg=msg), error

    # ERROR HANDLERS
    @app.errorhandler(Exception)
    def error_page(err):  # skipcq: PTC-W0065
        """
        Error handlers, if the error is not a HTTP error, return 500
        """
        if not isinstance(err, HTTPException):
            abort(500)
        return (
            render_template("error.html", error=err.code, msg=err.description),
            err.code,
        )

    # ASSETS
    assets.init_app(app)

    scripts = Bundle(
        "js/*.js", output="gen/js.js", depends="js/*.js"
    )  # filter jsmin is broken :c
    styles = Bundle(
        "sass/style.sass",
        filters="libsass, cssmin",
        output="gen/styles.css",
        depends="sass/**/*.sass",
    )

    assets.register("scripts", scripts)
    assets.register("styles", styles)

    # BLUEPRINTS
    app.register_blueprint(view_auth.blueprint)
    app.register_blueprint(view_index.blueprint)
    app.register_blueprint(view_image.blueprint)
    app.register_blueprint(view_group.blueprint)
    app.register_blueprint(view_profile.blueprint)
    app.register_blueprint(view_settings.blueprint)

    # APIS
    app.register_blueprint(api_media.blueprint)
    app.register_blueprint(api_group.blueprint)
    app.register_blueprint(api_account.blueprint)

    # FILTERS
    app.register_blueprint(filters.blueprint)

    # CACHE AND COMPRESS
    cache.init_app(app)
    compress.init_app(app)

    # Yupee! We got there :3
    print("Done!")
    logging.info("Gallery started successfully!")
    return app

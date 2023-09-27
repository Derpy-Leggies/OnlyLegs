"""
Onlylegs Gallery
This is the main app file, checks on app stability and runs all da shit
"""
import os
import logging

from flask import Flask, render_template, abort, request
from werkzeug.security import generate_password_hash
from werkzeug.exceptions import HTTPException
from flask_assets import Bundle
from flask_migrate import init as migrate_init


from onlylegs.extensions import db, migrate, login_manager, assets, compress, cache
from onlylegs.config import (
    INSTANCE_DIR,
    MIGRATIONS_DIR,
    APPLICATION_ROOT,
    DATABASE_NAME,
)
from onlylegs.models import Users

from onlylegs.views.index import blueprint as view_index
from onlylegs.views.image import blueprint as view_image
from onlylegs.views.group import blueprint as view_group
from onlylegs.views.settings import blueprint as view_settings
from onlylegs.views.profile import blueprint as view_profile
from onlylegs.api import blueprint as api
from onlylegs.auth import blueprint as view_auth
from onlylegs.filters import blueprint as filters


def set_logger():
    file_name = os.path.join(APPLICATION_ROOT, "only.log")
    logging_level = logging.INFO
    date_format = "%Y-%m-%d %H:%M:%S"
    log_format = "%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s"

    logging.getLogger("werkzeug").disabled = True
    logging.basicConfig(
        filename=file_name,
        level=logging_level,
        datefmt=date_format,
        format=log_format,
        encoding="utf-8",
    )


def create_db():
    path_to_database = os.path.join(INSTANCE_DIR, DATABASE_NAME)

    if not os.path.exists(path_to_database):
        print("Database not found, creating...")

        user = Users(
            username=app.config["ADMIN_CONF"]["username"],
            email=app.config["ADMIN_CONF"]["email"],
            password=generate_password_hash("changeme!", method="scrypt"),
        )

        with app.app_context():
            db.create_all()
            db.session.add(user)
            db.session.commit()
            migrate_init(directory=MIGRATIONS_DIR)

        print(
            "####################################################",
            "# DEFAULT ADMIN USER GENERATED WITH GIVEN USERNAME #",
            '# THE DEFAULT PASSWORD "changeme!" HAS BEEN USED,  #',
            "# PLEASE RESET IT IN THE SETTINGS!                 #",
            "####################################################",
            sep="\n",
        )

        return

    print("Database found, continuing...")


def set_login_manager():
    """
    LOGIN MANAGER
    can also set session_protection to "strong"
    this would protect against session hijacking
    """
    login_manager.init_app(app)
    login_manager.login_view = "onlylegs.index"

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.filter_by(alt_id=user_id).first()

    @login_manager.unauthorized_handler
    def unauthorized():
        error = 401
        msg = "You are not authorized to view this page!!!!"
        return render_template("error.html", error=error, msg=msg), error


def page_assets():
    """
    ASSETS
    bundles all the sass and js and minifies them
    """
    assets.init_app(app)

    page_scripts = Bundle(
        "js/*.js", filters="jsmin", output="gen/main.js", depends="js/*.js"
    )
    page_styling = Bundle(
        "sass/style.sass",
        filters="libsass, cssmin",
        output="gen/styles.css",
        depends="sass/**/*.sass",
    )

    assets.register("scripts", page_scripts)
    assets.register("styles", page_styling)


def handle_errors():
    """
    ERROR HANDLER
    handles all the errors and returns a nice error page
    Code errors are displayed as 500 errors so no
    sensitive information is leaked
    """

    @app.errorhandler(Exception)
    def error_page(err):
        if not isinstance(err, HTTPException):
            abort(500)

        if request.method == "GET":
            return (
                render_template("error.html", error=err.code, msg=err.description),
                err.code,
            )
        else:
            return str(err.code) + ": " + err.description, err.code


def register_blueprints():
    """
    BLUEPRINTS
    registers all the blueprints
    """
    app.register_blueprint(view_auth)
    app.register_blueprint(view_index)
    app.register_blueprint(view_image)
    app.register_blueprint(view_group)
    app.register_blueprint(view_profile)
    app.register_blueprint(view_settings)
    app.register_blueprint(api)
    app.register_blueprint(filters)


app = Flask(__name__, instance_path=INSTANCE_DIR)
app.config.from_pyfile("config.py")

db.init_app(app)
migrate.init_app(app, db, directory=MIGRATIONS_DIR)

create_db()

set_logger()
set_login_manager()
page_assets()
handle_errors()
register_blueprints()

cache.init_app(app)
compress.init_app(app)

logging.info("Gallery started successfully!")


if __name__ == "__main__":
    app.run()

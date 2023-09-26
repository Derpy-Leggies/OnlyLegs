"""
Onlylegs Gallery
This is the main app file, checks on app stability and runs all da shit
"""
import os
import logging

from flask_assets import Bundle
from flask_migrate import init as migrate_init
from flask import Flask, render_template, abort, request
from werkzeug.exceptions import HTTPException

from onlylegs.utils import startup
from onlylegs.extensions import db, migrate, login_manager, assets, compress, cache
from onlylegs.config import INSTANCE_DIR, MIGRATIONS_DIR, APPLICATION_ROOT
from onlylegs.models import Users

from onlylegs.views.index import blueprint as view_index
from onlylegs.views.image import blueprint as view_image
from onlylegs.views.group import blueprint as view_group
from onlylegs.views.settings import blueprint as view_settings
from onlylegs.views.profile import blueprint as view_profile
from onlylegs.api import blueprint as api
from onlylegs.auth import blueprint as view_auth
from onlylegs.filters import blueprint as filters


logging.getLogger("werkzeug").disabled = True
logging.basicConfig(
    filename=os.path.join(APPLICATION_ROOT, "only.log"),
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
    encoding="utf-8",
)


app = Flask(__name__, instance_path=INSTANCE_DIR)
app.config.from_pyfile("config.py")

db.init_app(app)
migrate.init_app(app, db, directory=MIGRATIONS_DIR)

# App Sanity Checks
startup.check_dirs()
startup.check_env()
startup.check_conf()

if not os.path.exists(os.path.join(INSTANCE_DIR, "gallery.sqlite3")):
    startup.make_admin_user(app)
    migrate_init(directory=MIGRATIONS_DIR)


# LOGIN MANAGER
# can also set session_protection to "strong"
# this would protect against session hijacking
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


# ERROR HANDLERS
@app.errorhandler(Exception)
def error_page(err):
    """
    Error handlers, if the error is not a HTTP error, return 500
    """
    if not isinstance(err, HTTPException):
        abort(500)

    if request.method == "GET":
        return (
            render_template("error.html", error=err.code, msg=err.description),
            err.code,
        )
    else:
        return str(err.code) + ": " + err.description, err.code


# ASSETS
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

# BLUEPRINTS
app.register_blueprint(view_auth)
app.register_blueprint(view_index)
app.register_blueprint(view_image)
app.register_blueprint(view_group)
app.register_blueprint(view_profile)
app.register_blueprint(view_settings)
app.register_blueprint(api)
app.register_blueprint(filters)

# CACHE AND COMPRESS
cache.init_app(app)
compress.init_app(app)

# Yupee! We got there :3
print("Done!")
logging.info("Gallery started successfully!")


if __name__ == "__main__":
    app.run()

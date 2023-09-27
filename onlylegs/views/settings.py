"""
OnlyLegs - Settings page
"""
import os
import pathlib
import re
import logging
from colorthief import ColorThief
from flask import (
    Blueprint,
    request,
    current_app,
    render_template,
    flash,
    redirect,
    url_for,
)
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from onlylegs.extensions import db
from onlylegs.models import Users


blueprint = Blueprint("settings", __name__, url_prefix="/settings")


@blueprint.route("/", methods=["GET"])
@login_required
def general():
    """
    General settings page
    """
    return render_template("settings.html")


@blueprint.route("/account/pfp", methods=["POST"])
@login_required
def account_picture():
    user_record = Users.query.filter_by(id=current_user.id).first()
    uploaded_file = request.files.get("file", None)
    if not uploaded_file:
        return "No file uploaded!", 400

    image_mime = pathlib.Path(uploaded_file.filename).suffix.replace(".", "").lower()
    image_name = str(user_record.id) + "_pfp." + image_mime
    image_path = os.path.join(current_app.config["PFP_FOLDER"], image_name)

    if image_mime not in current_app.config["ALLOWED_EXTENSIONS"].keys():
        logging.info("File extension not allowed: %s", image_mime)
        return "File extension not allowed", 403

    if user_record.picture:
        os.remove(os.path.join(current_app.config["PFP_FOLDER"], user_record.picture))
        cache_name = user_record.picture.rsplit(".")[0]
        for file in pathlib.Path(current_app.config["CACHE_FOLDER"]).glob(
            cache_name + "*"
        ):
            os.remove(file)

    uploaded_file.save(image_path)
    image_colours = ColorThief(image_path).get_color()

    user_record.colour = image_colours
    user_record.picture = image_name
    db.session.commit()

    return "File uploaded", 200


@blueprint.route("/account/banner", methods=["POST"])
@login_required
def account_banner():
    user_record = Users.query.filter_by(id=current_user.id).first()
    uploaded_file = request.files.get("file", None)
    if not uploaded_file:
        return "No file uploaded!", 400

    image_mime = pathlib.Path(uploaded_file.filename).suffix.replace(".", "").lower()
    image_name = str(user_record.id) + "_banner." + image_mime
    image_path = os.path.join(current_app.config["BANNER_FOLDER"], image_name)

    if image_mime not in current_app.config["ALLOWED_EXTENSIONS"].keys():
        logging.info("File extension not allowed: %s", image_mime)
        return "File extension not allowed", 403

    if user_record.banner:
        os.remove(os.path.join(current_app.config["BANNER_FOLDER"], user_record.banner))
        cache_name = user_record.banner.rsplit(".")[0]
        for file in pathlib.Path(current_app.config["CACHE_FOLDER"]).glob(
            cache_name + "*"
        ):
            os.remove(file)

    uploaded_file.save(image_path)
    user_record.banner = image_name
    db.session.commit()

    return "File uploaded", 200


@blueprint.route("/account/username", methods=["POST"])
@login_required
def account_username():
    user_record = Users.query.filter_by(id=current_user.id).first()
    new_username = request.form.get("username", "").strip()

    username_regex = re.compile(r"\b[A-Za-z0-9._-]+\b")

    if not new_username or not username_regex.match(new_username):
        return "Username is invalid", 400

    user_record.username = new_username
    db.session.commit()

    return "Username changed", 200


@blueprint.route("/account/email", methods=["POST"])
@login_required
def account_email():
    user_record = Users.query.filter_by(id=current_user.id).first()
    current_password = request.form.get("current", "").strip()
    new_email = request.form.get("email", "").strip()

    email_regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

    if not current_password or not new_email:
        return "Fill in all the fields!", 400
    if not email_regex.match(new_email):
        return "Email is invalid!", 400
    if not check_password_hash(user_record.password, current_password):
        return "Incorrect password!", 400

    user_record.email = new_email
    db.session.commit()

    return "Email changed", 200


@blueprint.route("/account/password", methods=["POST"])
@login_required
def account_password():
    user_record = Users.query.filter_by(id=current_user.id).first()
    current_password = request.form.get("current", "").strip()
    new_password = request.form.get("password", "").strip()
    new_confirm = request.form.get("confirm", "").strip()

    if not current_password or not new_password or not new_confirm:
        return "Fill in all the fields!", 400
    if new_password != new_confirm:
        return "Passwords do not match!", 400
    if not check_password_hash(user_record.password, current_password):
        return "Incorrect password!", 400

    user_record.password = generate_password_hash(new_password, method="scrypt")
    db.session.commit()

    flash(["Password changed! You must login now", 0])
    return redirect(url_for("auth.logout"))

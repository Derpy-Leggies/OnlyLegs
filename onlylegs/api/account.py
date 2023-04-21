"""
Onlylegs - API endpoints
"""
from uuid import uuid4
import os
import pathlib
import re
import logging

from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user

from colorthief import ColorThief

from onlylegs.extensions import db
from onlylegs.models import User


blueprint = Blueprint("account_api", __name__, url_prefix="/api/account")


@blueprint.route("/picture/<int:user_id>", methods=["POST"])
@login_required
def account_picture(user_id):
    """
    Returns the profile of a user
    """
    user = db.get_or_404(User, user_id)
    file = request.files["file"]

    # If no image is uploaded, return 404 error
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    elif user.id != current_user.id:
        return jsonify({"error": "You are not allowed to do this, go away"}), 403

    # Get file extension, generate random name and set file path
    img_ext = pathlib.Path(file.filename).suffix.replace(".", "").lower()
    img_name = str(user.id)
    img_path = os.path.join(current_app.config["PFP_FOLDER"], img_name + "." + img_ext)

    # Check if file extension is allowed
    if img_ext not in current_app.config["ALLOWED_EXTENSIONS"].keys():
        logging.info("File extension not allowed: %s", img_ext)
        return jsonify({"error": "File extension not allowed"}), 403

    if user.picture:
        # Delete cached files and old image
        os.remove(os.path.join(current_app.config["PFP_FOLDER"], user.picture))
        cache_name = user.picture.rsplit(".")[0]
        for cache_file in pathlib.Path(current_app.config["CACHE_FOLDER"]).glob(
            cache_name + "*"
        ):
            os.remove(cache_file)

    # Save file
    try:
        file.save(img_path)
    except OSError as err:
        logging.info("Error saving file %s because of %s", img_path, err)
        return jsonify({"error": "Error saving file"}), 500

    img_colors = ColorThief(img_path).get_color()

    # Save to database
    user.colour = img_colors
    user.picture = str(img_name + "." + img_ext)
    db.session.commit()

    return jsonify({"message": "File uploaded"}), 200


@blueprint.route("/username/<int:user_id>", methods=["POST"])
@login_required
def account_username(user_id):
    """
    Returns the profile of a user
    """
    user = db.get_or_404(User, user_id)
    new_name = request.form["name"]

    username_regex = re.compile(r"\b[A-Za-z0-9._-]+\b")

    # Validate the form
    if not new_name or not username_regex.match(new_name):
        return jsonify({"error": "Username is invalid"}), 400
    elif user.id != current_user.id:
        return jsonify({"error": "You are not allowed to do this, go away"}), 403

    # Save to database
    user.username = new_name
    db.session.commit()

    return jsonify({"message": "Username changed"}), 200

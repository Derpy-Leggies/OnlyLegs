"""
Onlylegs - API endpoints
"""
import os
import pathlib
import re
import logging
from uuid import uuid4

from flask import (
    Blueprint,
    flash,
    abort,
    send_from_directory,
    jsonify,
    request,
    current_app,
)
from flask_login import login_required, current_user

from colorthief import ColorThief

from onlylegs.extensions import db
from onlylegs.models import Users, Pictures, Albums, AlbumJunction
from onlylegs.utils.metadata import yoink
from onlylegs.utils.generate_image import generate_thumbnail


blueprint = Blueprint("api", __name__, url_prefix="/api")


@blueprint.route("/account/picture/<int:user_id>", methods=["POST"])
@login_required
def account_picture(user_id):
    """
    Returns the profile of a user
    """
    user = db.get_or_404(Users, user_id)
    file = request.files.get("file", None)

    # If no image is uploaded, return 404 error
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    if user.id != current_user.id:
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


@blueprint.route("/account/username/<int:user_id>", methods=["POST"])
@login_required
def account_username(user_id):
    """
    Returns the profile of a user
    """
    user = db.get_or_404(Users, user_id)
    new_name = request.form["name"]

    username_regex = re.compile(r"\b[A-Za-z0-9._-]+\b")

    # Validate the form
    if not new_name or not username_regex.match(new_name):
        return jsonify({"error": "Username is invalid"}), 400
    if user.id != current_user.id:
        return jsonify({"error": "You are not allowed to do this, go away"}), 403

    # Save to database
    user.username = new_name
    db.session.commit()

    return jsonify({"message": "Username changed"}), 200


@blueprint.route("/media/<path:path>", methods=["GET"])
def media(path):
    """
    Returns image from media folder
    r for resolution, thumb for thumbnail etc
    e for extension, jpg, png etc
    """
    res = request.args.get("r", default=None).strip()
    ext = request.args.get("e", default=None).strip()

    # if no args are passed, return the raw file
    if not res and not ext:
        if not os.path.exists(os.path.join(current_app.config["MEDIA_FOLDER"], path)):
            abort(404)
        return send_from_directory(current_app.config["MEDIA_FOLDER"], path)

    # Generate thumbnail, if None is returned a server error occured
    thumb = generate_thumbnail(path, res, ext)
    if not thumb:
        abort(500)

    response = send_from_directory(os.path.dirname(thumb), os.path.basename(thumb))
    response.headers["Cache-Control"] = "public, max-age=31536000"
    response.headers["Expires"] = "31536000"

    return response


@blueprint.route("/media/upload", methods=["POST"])
@login_required
def upload():
    """
    Uploads an image to the server and saves it to the database
    """
    form_file = request.files.get("file", None)
    form = request.form

    if not form_file:
        return jsonify({"message": "No file"}), 400

    # Get file extension, generate random name and set file path
    img_ext = pathlib.Path(form_file.filename).suffix.replace(".", "").lower()
    img_name = "GWAGWA_" + str(uuid4())
    img_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"], img_name + "." + img_ext
    )

    # Check if file extension is allowed
    if img_ext not in current_app.config["ALLOWED_EXTENSIONS"].keys():
        logging.info("File extension not allowed: %s", img_ext)
        return jsonify({"message": "File extension not allowed"}), 403

    # Save file
    try:
        form_file.save(img_path)
    except OSError as err:
        logging.info("Error saving file %s because of %s", img_path, err)
        return jsonify({"message": "Error saving file"}), 500

    img_exif = yoink(img_path)  # Get EXIF data
    img_colors = ColorThief(img_path).get_palette(color_count=3)  # Get color palette

    # Save to database
    query = Pictures(
        author_id=current_user.id,
        filename=img_name + "." + img_ext,
        mimetype=img_ext,
        exif=img_exif,
        colours=img_colors,
        description=form["description"],
        alt=form["alt"],
    )

    db.session.add(query)
    db.session.commit()

    return jsonify({"message": "File uploaded"}), 200


@blueprint.route("/media/delete/<int:image_id>", methods=["POST"])
@login_required
def delete_image(image_id):
    """
    Deletes an image from the server and database
    """
    post = db.get_or_404(Pictures, image_id)

    # Check if image exists and if user is allowed to delete it (author)
    if post.author_id != current_user.id:
        logging.info("User %s tried to delete image %s", current_user.id, image_id)
        return (
            jsonify({"message": "You are not allowed to delete this image, heck off"}),
            403,
        )

    # Delete file
    try:
        os.remove(os.path.join(current_app.config["UPLOAD_FOLDER"], post.filename))
    except FileNotFoundError:
        logging.warning(
            "File not found: %s, already deleted or never existed", post.filename
        )

    # Delete cached files
    cache_name = post.filename.rsplit(".")[0]
    for cache_file in pathlib.Path(current_app.config["CACHE_FOLDER"]).glob(
        cache_name + "*"
    ):
        os.remove(cache_file)

    AlbumJunction.query.filter_by(picture_id=image_id).delete()
    db.session.delete(post)
    db.session.commit()

    logging.info("Removed image (%s) %s", image_id, post.filename)
    flash(["Image was all in Le Head!", "1"])
    return jsonify({"message": "Image deleted"}), 200


@blueprint.route("/group/create", methods=["POST"])
@login_required
def create_group():
    """
    Creates a group
    """
    group_name = request.form.get("name", "").strip()
    group_description = request.form.get("description", "").strip()
    group_author = current_user.id

    new_group = Albums(
        name=group_name,
        description=group_description,
        author_id=group_author,
    )

    db.session.add(new_group)
    db.session.commit()

    return jsonify({"message": "Group created", "id": new_group.id})


@blueprint.route("/group/modify", methods=["POST"])
@login_required
def modify_group():
    """
    Changes the images in a group
    """
    group_id = request.form.get("group", "").strip()
    image_id = request.form.get("image", "").strip()
    action = request.form.get("action", "").strip()

    group = db.get_or_404(Albums, group_id)
    db.get_or_404(Pictures, image_id)  # Check if image exists

    if group.author_id != current_user.id:
        return jsonify({"message": "You are not the owner of this group"}), 403

    junction_exist = AlbumJunction.query.filter_by(
        album_id=group_id, picture_id=image_id
    ).first()

    if action == "add" and not junction_exist:
        db.session.add(AlbumJunction(album_id=group_id, picture_id=image_id))
    elif request.form["action"] == "remove":
        AlbumJunction.query.filter_by(album_id=group_id, picture_id=image_id).delete()

    db.session.commit()
    return jsonify({"message": "Group modified"})


@blueprint.route("/group/delete", methods=["POST"])
def delete_group():
    """
    Deletes a group
    """
    group_id = request.form.get("group", "").strip()
    group = db.get_or_404(Albums, group_id)

    if group.author_id != current_user.id:
        return jsonify({"message": "You are not the owner of this group"}), 403

    AlbumJunction.query.filter_by(album_id=group_id).delete()
    db.session.delete(group)
    db.session.commit()

    flash(["Group yeeted!", "1"])
    return jsonify({"message": "Group deleted"})

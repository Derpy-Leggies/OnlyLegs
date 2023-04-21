"""
Onlylegs - API endpoints
"""
from uuid import uuid4
import os
import pathlib
import re
import logging

from flask import Blueprint, send_from_directory, abort, flash, request, current_app
from flask_login import login_required, current_user

from colorthief import ColorThief

from onlylegs.extensions import db
from onlylegs.models import Post, Group, GroupJunction, User
from onlylegs.utils import metadata as mt
from onlylegs.utils.generate_image import generate_thumbnail


blueprint = Blueprint("api", __name__, url_prefix="/api")


@blueprint.route("/media/<path:path>", methods=["GET"])
def media(path):
    """
    Returns a file from the uploads folder
    r for resolution, thumb for thumbnail etc
    e for extension, jpg, png etc
    """
    res = request.args.get("r", default=None, type=str)
    ext = request.args.get("e", default=None, type=str)
    # path = secure_filename(path)

    # if no args are passed, return the raw file
    if not res and not ext:
        if not os.path.exists(os.path.join(current_app.config["MEDIA_FOLDER"], path)):
            abort(404)
        return send_from_directory(current_app.config["MEDIA_FOLDER"], path)

    thumb = generate_thumbnail(path, res, ext)
    if not thumb:
        abort(404)

    return send_from_directory(os.path.dirname(thumb), os.path.basename(thumb))


@blueprint.route("/upload", methods=["POST"])
@login_required
def upload():
    """
    Uploads an image to the server and saves it to the database
    """
    form_file = request.files["file"]
    form = request.form

    # If no image is uploaded, return 404 error
    if not form_file:
        return abort(404)

    # Get file extension, generate random name and set file path
    img_ext = pathlib.Path(form_file.filename).suffix.replace(".", "").lower()
    img_name = "GWAGWA_" + str(uuid4())
    img_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"], img_name + "." + img_ext
    )

    # Check if file extension is allowed
    if img_ext not in current_app.config["ALLOWED_EXTENSIONS"].keys():
        logging.info("File extension not allowed: %s", img_ext)
        abort(403)

    # Save file
    try:
        form_file.save(img_path)
    except OSError as err:
        logging.info("Error saving file %s because of %s", img_path, err)
        abort(500)

    img_exif = mt.Metadata(img_path).yoink()  # Get EXIF data
    img_colors = ColorThief(img_path).get_palette(color_count=3)  # Get color palette

    # Save to database
    query = Post(
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

    return "Gwa Gwa"  # Return something so the browser doesn't show an error


@blueprint.route("/delete/<int:image_id>", methods=["POST"])
@login_required
def delete_image(image_id):
    """
    Deletes an image from the server and database
    """
    post = db.get_or_404(Post, image_id)

    # Check if image exists and if user is allowed to delete it (author)
    if post.author_id != current_user.id:
        abort(403)

    # Delete file
    try:
        os.remove(os.path.join(current_app.config["UPLOAD_FOLDER"], post.filename))
    except FileNotFoundError:
        logging.warning(
            "File not found: %s, already deleted or never existed", post.filename
        )

    # Delete cached files
    cache_name = post.filename.rsplit(".")[0]
    for cache_file in pathlib.Path(current_app.config["CACHE_FOLDER"]).glob(cache_name + "*"):
        os.remove(cache_file)

    GroupJunction.query.filter_by(post_id=image_id).delete()
    db.session.delete(post)
    db.session.commit()

    logging.info("Removed image (%s) %s", image_id, post.filename)
    flash(["Image was all in Le Head!", "1"])
    return "Gwa Gwa"


@blueprint.route("/group/create", methods=["POST"])
@login_required
def create_group():
    """
    Creates a group
    """
    new_group = Group(
        name=request.form["name"],
        description=request.form["description"],
        author_id=current_user.id,
    )

    db.session.add(new_group)
    db.session.commit()

    return ":3"


@blueprint.route("/group/modify", methods=["POST"])
@login_required
def modify_group():
    """
    Changes the images in a group
    """
    group_id = request.form["group"]
    image_id = request.form["image"]
    action = request.form["action"]

    group = db.get_or_404(Group, group_id)
    db.get_or_404(Post, image_id)  # Check if image exists

    if group.author_id != current_user.id:
        abort(403)

    if (
        action == "add"
        and not GroupJunction.query.filter_by(
            group_id=group_id, post_id=image_id
        ).first()
    ):
        db.session.add(GroupJunction(group_id=group_id, post_id=image_id))
    elif request.form["action"] == "remove":
        GroupJunction.query.filter_by(group_id=group_id, post_id=image_id).delete()

    db.session.commit()
    return ":3"


@blueprint.route("/group/delete", methods=["POST"])
def delete_group():
    """
    Deletes a group
    """
    group_id = request.form["group"]
    group = db.get_or_404(Group, group_id)

    if group.author_id != current_user.id:
        abort(403)

    GroupJunction.query.filter_by(group_id=group_id).delete()
    db.session.delete(group)
    db.session.commit()

    flash(["Group yeeted!", "1"])
    return ":3"


@blueprint.route("/user/picture/<int:user_id>", methods=["POST"])
def user_picture(user_id):
    """
    Returns the profile of a user
    """
    user = db.get_or_404(User, user_id)
    file = request.files["file"]

    # If no image is uploaded, return 404 error
    if not file:
        return abort(404)
    elif user.id != current_user.id:
        return abort(403)

    # Get file extension, generate random name and set file path
    img_ext = pathlib.Path(file.filename).suffix.replace(".", "").lower()
    img_name = str(user.id)
    img_path = os.path.join(current_app.config["PFP_FOLDER"], img_name + "." + img_ext)

    # Check if file extension is allowed
    if img_ext not in current_app.config["ALLOWED_EXTENSIONS"].keys():
        logging.info("File extension not allowed: %s", img_ext)
        abort(403)
        
    if user.picture:
        os.remove(os.path.join(current_app.config["PFP_FOLDER"], user.picture))
        # Delete cached files
        cache_name = user.picture.rsplit(".")[0]
        for cache_file in pathlib.Path(current_app.config["CACHE_FOLDER"]).glob(cache_name + "*"):
            os.remove(cache_file)

    # Save file
    try:
        file.save(img_path)
    except OSError as err:
        logging.info("Error saving file %s because of %s", img_path, err)
        abort(500)

    img_colors = ColorThief(img_path).get_color()  # Get color palette

    # Save to database
    user.colour = img_colors
    user.picture = str(img_name + "." + img_ext)
    db.session.commit()

    return "Gwa Gwa"  # Return something so the browser doesn't show an error

@blueprint.route("/user/username/<int:user_id>", methods=["POST"])
def user_username(user_id):
    """
    Returns the profile of a user
    """
    user = db.get_or_404(User, user_id)
    new_name = request.form["name"]
    
    username_regex = re.compile(r"\b[A-Za-z0-9._-]+\b")

    # Validate the form
    if not new_name or not username_regex.match(new_name):
        abort(400)
    elif user.id != current_user.id:
        return abort(403)
    
    # Save to database
    user.username = new_name
    db.session.commit()

    return "Gwa Gwa"  # Return something so the browser doesn't show an error
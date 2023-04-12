"""
Onlylegs - API endpoints
"""
from uuid import uuid4
import os
import pathlib
import logging
import platformdirs

from flask import Blueprint, send_from_directory, abort, flash, request, current_app
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

from colorthief import ColorThief

from onlylegs.extensions import db
from onlylegs.models import Post, Group, GroupJunction
from onlylegs.utils import metadata as mt
from onlylegs.utils.generate_image import generate_thumbnail


blueprint = Blueprint("api", __name__, url_prefix="/api")


@blueprint.route("/file/<file_name>", methods=["GET"])
def file(file_name):
    """
    Returns a file from the uploads folder
    r for resolution, 400x400 or thumb for thumbnail
    """
    res = request.args.get("r", default=None, type=str)  # Type of file (thumb, etc)
    ext = request.args.get("e", default=None, type=str)  # File extension
    file_name = secure_filename(file_name)  # Sanitize file name

    # if no args are passed, return the raw file
    if not res and not ext:
        if not os.path.exists(
            os.path.join(current_app.config["UPLOAD_FOLDER"], file_name)
        ):
            abort(404)
        return send_from_directory(current_app.config["UPLOAD_FOLDER"], file_name)

    thumb = generate_thumbnail(file_name, res, ext)
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
    post = Post.query.filter_by(id=image_id).first()

    # Check if image exists and if user is allowed to delete it (author)
    if post is None:
        abort(404)
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
    cache_path = os.path.join(platformdirs.user_config_dir("onlylegs"), "cache")
    cache_name = post.filename.rsplit(".")[0]
    for cache_file in pathlib.Path(cache_path).glob(cache_name + "*"):
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
    group = Group.query.filter_by(id=group_id).first()

    if group is None:
        abort(404)
    elif group.author_id != current_user.id:
        abort(403)

    GroupJunction.query.filter_by(group_id=group_id).delete()
    db.session.delete(group)
    db.session.commit()

    flash(["Group yeeted!", "1"])
    return ":3"

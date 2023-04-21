"""
Onlylegs - API endpoints
Media upload and retrieval
"""
import os
from uuid import uuid4
import os
import pathlib
import logging

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
from onlylegs.models import Post, GroupJunction
from onlylegs.utils import metadata as mt
from onlylegs.utils.generate_image import generate_thumbnail


blueprint = Blueprint("media_api", __name__, url_prefix="/api/media")


@blueprint.route("/<path:path>", methods=["GET"])
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
        abort(500)

    return send_from_directory(os.path.dirname(thumb), os.path.basename(thumb))


@blueprint.route("/upload", methods=["POST"])
@login_required
def upload():
    """
    Uploads an image to the server and saves it to the database
    """
    form_file = request.files["file"]
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

    return jsonify({"message": "File uploaded"}), 200


@blueprint.route("/delete/<int:image_id>", methods=["POST"])
@login_required
def delete_image(image_id):
    """
    Deletes an image from the server and database
    """
    post = db.get_or_404(Post, image_id)

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

    GroupJunction.query.filter_by(post_id=image_id).delete()
    db.session.delete(post)
    db.session.commit()

    logging.info("Removed image (%s) %s", image_id, post.filename)
    flash(["Image was all in Le Head!", "1"])
    return jsonify({"message": "Image deleted"}), 200

"""
Onlylegs - API endpoints
"""
import os
import pathlib
import logging
from uuid import uuid4

from PIL import Image
from PIL.ExifTags import TAGS

from flask import (
    Blueprint,
    abort,
    send_from_directory,
    jsonify,
    request,
    current_app,
)
from flask_login import login_required, current_user

from colorthief import ColorThief

from onlylegs.extensions import db
from onlylegs.models import Pictures, Exif
from onlylegs.utils.generate_image import generate_thumbnail


blueprint = Blueprint("api", __name__, url_prefix="/api")


@blueprint.route("/media/<path:path>", methods=["GET"])
def media(path):
    """
    Returns image from media folder
    r for resolution, thumb for thumbnail etc
    e for extension, jpg, png etc
    """
    res = request.args.get("r", "").strip()
    ext = request.args.get("e", "").strip()

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
    image_description = request.form.get("description", "").strip()
    image_alt = request.form.get("alt", "").strip()
    image_file = request.files.get("file", None)

    if not image_file:
        return jsonify({"message": "No file"}), 400

    # Get file extension, generate random name and set file path
    image_mime = pathlib.Path(image_file.filename).suffix.replace(".", "").lower()
    image_name = "GWAGWA_" + str(uuid4())
    image_filename = image_name + "." + image_mime
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], image_filename)

    if image_mime not in current_app.config["ALLOWED_EXTENSIONS"].keys():
        logging.info("File extension not allowed: %s", image_mime)
        return jsonify({"message": "File extension not allowed"}), 403

    image_file.save(save_path)

    image_colours = ColorThief(save_path).get_palette(color_count=3)

    image_record = Pictures(
        author_id=current_user.id,
        filename=image_filename,
        mimetype=image_mime,
        colours=image_colours,
        description=image_description,
        alt=image_alt,
    )
    db.session.add(image_record)
    db.session.commit()

    image_exif = []
    with Image.open(save_path) as file:
        image_exif.append(
            Exif(
                picture_id=image_record.id,
                key="FileName",
                value=image_filename,
            )
        )
        image_exif.append(
            Exif(
                picture_id=image_record.id,
                key="FileSize",
                value=os.path.getsize(save_path),
            )
        )
        image_exif.append(
            Exif(
                picture_id=image_record.id,
                key="FileFormat",
                value=image_mime,
            )
        )
        image_exif.append(
            Exif(
                picture_id=image_record.id,
                key="FileWidth",
                value=file.size[0],
            )
        )
        image_exif.append(
            Exif(
                picture_id=image_record.id,
                key="FileHeight",
                value=file.size[1],
            )
        )

        try:
            tags = file._getexif()
            for tag, value in TAGS.items():
                if tag in tags:
                    image_exif.append(
                        Exif(
                            picture_id=image_record.id,
                            key=value,
                            value=tags[tag],
                        )
                    )
        except TypeError:
            pass

    db.session.add_all(image_exif)
    db.session.commit()

    return jsonify({"message": "File uploaded"}), 200

"""
Onlylegs - Image View
"""
import os
import logging
import pathlib
from math import ceil
from flask import (
    Blueprint,
    render_template,
    url_for,
    current_app,
    request,
    flash,
    jsonify,
)
from flask_login import current_user
from onlylegs.models import Pictures, AlbumJunction, Albums, Exif
from onlylegs.extensions import db


blueprint = Blueprint("image", __name__, url_prefix="/image")


@blueprint.route("/<int:image_id>", methods=["GET"])
def image(image_id):
    """
    Image view, shows the image and its metadata
    """
    # Get the image, if it doesn't exist, 404
    image_record = db.get_or_404(Pictures, image_id, description="Image not found :<")
    image_record_exif = Exif.query.filter(Exif.picture_id == image_id).all()

    # Get all groups the image is in
    groups = (
        AlbumJunction.query.with_entities(AlbumJunction.album_id)
        .filter(AlbumJunction.picture_id == image_id)
        .all()
    )

    # Get the group data for each group the image is in
    image_record.groups = []
    for group in groups:
        image_record.groups.append(
            Albums.query.with_entities(Albums.id, Albums.name)
            .filter(Albums.id == group[0])
            .first()
        )

    # Get the next and previous images
    # Check if there is a group ID set
    next_url = (
        Pictures.query.with_entities(Pictures.id)
        .filter(Pictures.id > image_id)
        .order_by(Pictures.id.asc())
        .first()
    )
    prev_url = (
        Pictures.query.with_entities(Pictures.id)
        .filter(Pictures.id < image_id)
        .order_by(Pictures.id.desc())
        .first()
    )

    # If there is a next or previous image, get the url
    next_url = url_for("image.image", image_id=next_url[0]) if next_url else None
    prev_url = url_for("image.image", image_id=prev_url[0]) if prev_url else None

    # Yoink all the images in the database
    total_images = (
        Pictures.query.with_entities(Pictures.id).order_by(Pictures.id.desc()).all()
    )
    limit = current_app.config["UPLOAD_CONF"]["max-load"]

    # If the number of items is less than the limit, no point of calculating the page
    return_page = None
    if len(total_images) > limit:
        # How many pages should there be
        for i in range(ceil(len(total_images) / limit)):
            # Slice the list of IDs into chunks of the limit
            for j in total_images[i * limit : (i + 1) * limit]:
                # Is our image in this chunk?
                if not image_id > j[-1]:
                    return_page = i + 1
                    break

    close_tab = True
    if request.cookies.get("image-info") == "0":
        close_tab = False

    return render_template(
        "image.html",
        image=image_record,
        image_exif=image_record_exif,
        next_url=next_url,
        prev_url=prev_url,
        return_page=return_page,
        close_tab=close_tab,
    )


@blueprint.route("/<int:image_id>", methods=["PUT"])
def image_put(image_id):
    """
    Update the image metadata
    """
    image_record = db.get_or_404(Pictures, image_id, description="Image not found :<")

    image_record.description = request.form.get("description", image_record.description)
    image_record.alt = request.form.get("alt", image_record.alt)

    print(request.form.get("description"))

    db.session.commit()

    flash(["Image updated!", "1"])
    return "OK", 200


@blueprint.route("/<int:image_id>", methods=["DELETE"])
def image_delete(image_id):
    image_record = db.get_or_404(Pictures, image_id)

    # Check if image exists and if user is allowed to delete it (author)
    if image_record.author_id != current_user.id:
        logging.info("User %s tried to delete image %s", current_user.id, image_id)
        return (
            jsonify({"message": "You are not allowed to delete this image, heck off"}),
            403,
        )

    # Delete file
    try:
        os.remove(
            os.path.join(current_app.config["UPLOAD_FOLDER"], image_record.filename)
        )
    except FileNotFoundError:
        logging.warning(
            "File not found: %s, already deleted or never existed",
            image_record.filename,
        )

    # Delete cached files
    cache_name = image_record.filename.rsplit(".")[0]
    for cache_file in pathlib.Path(current_app.config["CACHE_FOLDER"]).glob(
        cache_name + "*"
    ):
        os.remove(cache_file)

    AlbumJunction.query.filter_by(picture_id=image_id).delete()
    db.session.delete(image_record)
    db.session.commit()

    logging.info("Removed image (%s) %s", image_id, image_record.filename)
    flash(["Image was all in Le Head!", "1"])
    return jsonify({"message": "Image deleted"}), 200

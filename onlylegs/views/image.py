"""
Onlylegs - Image View
"""
from math import ceil
from flask import Blueprint, render_template, url_for, current_app, request
from onlylegs.models import Pictures, AlbumJunction, Albums
from onlylegs.extensions import db


blueprint = Blueprint("image", __name__, url_prefix="/image")


@blueprint.route("/<int:image_id>")
def image(image_id):
    """
    Image view, shows the image and its metadata
    """
    # Get the image, if it doesn't exist, 404
    image = db.get_or_404(Pictures, image_id, description="Image not found :<")

    # Get all groups the image is in
    groups = (
        AlbumJunction.query.with_entities(AlbumJunction.album_id)
        .filter(AlbumJunction.picture_id == image_id)
        .all()
    )

    # Get the group data for each group the image is in
    image.groups = []
    for group in groups:
        image.groups.append(
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
    if next_url:
        next_url = url_for("image.image", image_id=next_url[0])
    if prev_url:
        prev_url = url_for("image.image", image_id=prev_url[0])

    # Yoink all the images in the database
    total_images = (
        Pictures.query.with_entities(Pictures.id).order_by(Pictures.id.desc()).all()
    )
    limit = current_app.config["UPLOAD_CONF"]["max-load"]

    # If the number of items is less than the limit, no point of calculating the page
    if len(total_images) <= limit:
        return_page = None
    else:
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
        image=image,
        next_url=next_url,
        prev_url=prev_url,
        return_page=return_page,
        close_tab=close_tab,
    )

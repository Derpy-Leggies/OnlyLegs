"""
Onlylegs - Image View
"""
from math import ceil

from flask import Blueprint, abort, render_template, url_for, current_app

from gallery.models import Posts, Users, GroupJunction, Groups


blueprint = Blueprint("image", __name__, url_prefix="/image")


@blueprint.route("/<int:image_id>")
def image(image_id):
    """
    Image view, shows the image and its metadata
    """
    # Get the image, if it doesn't exist, 404
    image = Posts.query.filter(Posts.id == image_id).first()
    if not image:
        abort(404, "Image not found :<")

    # Get the image's author username
    image.author_username = (
        Users.query.with_entities(Users.username)
        .filter(Users.id == image.author_id)
        .first()[0]
    )

    # Get the image's groups
    groups = (
        GroupJunction.query.with_entities(GroupJunction.group_id)
        .filter(GroupJunction.post_id == image_id)
        .all()
    )

    # For each group, get the group data and add it to the image item
    image.groups = []
    for group in groups:
        image.groups.append(
            Groups.query.with_entities(Groups.name, Groups.id)
            .filter(Groups.id == group[0])
            .first()
        )

    # Get the next and previous images
    # Check if there is a group ID set
    next_url = (
        Posts.query.with_entities(Posts.id)
        .filter(Posts.id > image_id)
        .order_by(Posts.id.asc())
        .first()
    )
    prev_url = (
        Posts.query.with_entities(Posts.id)
        .filter(Posts.id < image_id)
        .order_by(Posts.id.desc())
        .first()
    )

    # If there is a next or previous image, get the url
    if next_url:
        next_url = url_for("image.image", image_id=next_url[0])
    if prev_url:
        prev_url = url_for("image.image", image_id=prev_url[0])

    # Yoink all the images in the database
    total_images = Posts.query.with_entities(Posts.id).order_by(Posts.id.desc()).all()
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
                if image_id < j[-1]:
                    return_page = i + 1
                    break

    return render_template(
        "image.html",
        image=image,
        next_url=next_url,
        prev_url=prev_url,
        return_page=return_page,
    )

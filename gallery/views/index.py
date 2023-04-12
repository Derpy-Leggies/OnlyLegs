"""
Onlylegs Gallery - Index view
"""
from math import ceil

from flask import Blueprint, render_template, request, current_app
from werkzeug.exceptions import abort

from gallery.models import Post


blueprint = Blueprint("gallery", __name__)


@blueprint.route("/")
def index():
    """
    Home page of the website, shows the feed of the latest images
    """
    # meme
    if request.args.get("coffee") == "please":
        abort(418)

    # pagination, defaults to page 1 if no page is specified
    page = request.args.get("page", default=1, type=int)
    limit = current_app.config["UPLOAD_CONF"]["max-load"]

    # get the total number of images in the database
    # calculate the total number of pages, and make sure the page number is valid
    total_images = Post.query.with_entities(Post.id).count()
    pages = ceil(max(total_images, limit) / limit)
    if page > pages:
        abort(
            404,
            "You have reached the far and beyond, "
            + "but you will not find your answers here.",
        )

    # get the images for the current page
    images = (
        Post.query.with_entities(
            Post.filename, Post.alt, Post.colours, Post.created_at, Post.id
        )
        .order_by(Post.id.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return render_template(
        "index.html", images=images, total_images=total_images, pages=pages, page=page
    )

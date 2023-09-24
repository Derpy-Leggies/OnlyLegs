"""
Onlylegs Gallery - Index view
"""
from math import ceil
from flask import Blueprint, render_template, request, current_app
from werkzeug.exceptions import abort
from onlylegs.models import Pictures, Users


blueprint = Blueprint("gallery", __name__)


@blueprint.route("/")
def index():
    """
    Home page of the website, shows the feed of the latest images
    """
    # pagination, defaults to page 1 if no page is specified
    page = request.args.get("page", default=1, type=int)
    limit = current_app.config["UPLOAD_CONF"]["max-load"]

    # get the total number of images in the database
    # calculate the total number of pages, and make sure the page number is valid
    total_images = Pictures.query.with_entities(Pictures.id).count()
    pages = ceil(max(total_images, limit) / limit)
    if page > pages:
        return abort(
            404,
            "You have reached the far and beyond, but you will not find your answers here.",
        )

    # get the images for the current page
    images = (
        Pictures.query.with_entities(
            Pictures.filename,
            Pictures.alt,
            Pictures.colours,
            Pictures.created_at,
            Pictures.id,
            Users.username,
        )
        .join(Users)
        .order_by(Pictures.id.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return render_template(
        "index.html", images=images, total_images=total_images, pages=pages, page=page
    )

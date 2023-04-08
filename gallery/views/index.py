"""
Onlylegs Gallery - Index view
"""
from math import ceil

from flask import Blueprint, render_template, request, current_app
from werkzeug.exceptions import abort

from sqlalchemy.orm import sessionmaker
from gallery import db


blueprint = Blueprint("gallery", __name__)
db_session = sessionmaker(bind=db.engine)
db_session = db_session()


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
    total_images = db_session.query(db.Posts.id).count()
    pages = ceil(max(total_images, limit) / limit)
    if page > pages:
        abort(
            404,
            "You have reached the far and beyond, "
            + "but you will not find your answers here.",
        )

    # get the images for the current page
    images = (
        db_session.query(
            db.Posts.filename,
            db.Posts.alt,
            db.Posts.colours,
            db.Posts.created_at,
            db.Posts.id,
        )
        .order_by(db.Posts.id.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return render_template(
        "index.html", images=images, total_images=total_images, pages=pages, page=page
    )

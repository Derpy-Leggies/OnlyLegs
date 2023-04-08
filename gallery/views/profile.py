"""
Onlylegs Gallery - Profile view
"""
from flask import Blueprint, render_template, request
from werkzeug.exceptions import abort
from flask_login import current_user

from sqlalchemy.orm import sessionmaker
from gallery import db


blueprint = Blueprint("profile", __name__, url_prefix="/profile")
db_session = sessionmaker(bind=db.engine)
db_session = db_session()


@blueprint.route("/profile")
def profile():
    """
    Profile overview, shows all profiles on the onlylegs gallery
    """
    user_id = request.args.get("id", default=None, type=int)

    # If there is no userID set, check if the user is logged in and display their profile
    if not user_id:
        if current_user.is_authenticated:
            user_id = current_user.id
        else:
            abort(404, "You must be logged in to view your own profile!")

    # Get the user's data
    user = db_session.query(db.Users).filter(db.Users.id == user_id).first()

    if not user:
        abort(404, "User not found :c")

    images = db_session.query(db.Posts).filter(db.Posts.author_id == user_id).all()

    return render_template("profile.html", user=user, images=images)

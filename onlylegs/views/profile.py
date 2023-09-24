"""
Onlylegs Gallery - Profile view
"""
from flask import Blueprint, render_template, request
from werkzeug.exceptions import abort
from flask_login import current_user

from onlylegs.models import Pictures, Users, Albums
from onlylegs.extensions import db


blueprint = Blueprint("profile", __name__, url_prefix="/profile")


@blueprint.route("/")
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
    user = db.get_or_404(Users, user_id, description="User not found :<")

    images = Pictures.query.filter(Pictures.author_id == user_id).all()
    groups = Albums.query.filter(Albums.author_id == user_id).all()

    return render_template("profile.html", user=user, images=images, groups=groups)

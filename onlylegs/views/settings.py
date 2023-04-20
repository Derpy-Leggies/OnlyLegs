"""
OnlyLegs - Settings page
"""
from flask import Blueprint, render_template
from flask_login import login_required


blueprint = Blueprint("settings", __name__, url_prefix="/settings")


@blueprint.route("/")
@login_required
def general():
    """
    General settings page
    """
    return render_template("settings.html")
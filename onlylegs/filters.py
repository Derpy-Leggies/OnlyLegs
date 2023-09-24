"""
OnlyLegs filters
Custom Jinja2 filters
"""
from flask import Blueprint
from onlylegs.utils import colour as colour_utils


blueprint = Blueprint("filters", __name__)


@blueprint.app_template_filter()
def colour_contrast(colour):
    """
    Pass in the colour of the background and will return
    a css variable based on the contrast of text required to be readable
    "color: var(--fg-white);" or "color: var(--fg-black);"
    """
    colour_obj = colour_utils.Colour(colour)
    return "rgb(var(--fg-black));" if colour_obj.is_light() else "rgb(var(--fg-white));"

"""
OnlyLegs filters
Custom Jinja2 filters
"""
from flask import Blueprint
from onlylegs.utils.colour import contrast


blueprint = Blueprint("filters", __name__)


@blueprint.app_template_filter()
def colour_contrast(colour):
    """
    Pass in the colour of the background and will return
    a css variable based on the contrast of text required to be readable
    "color: var(--fg-white);" or "color: var(--fg-black);"
    """
    bright = "var(--fg-white)"
    dark = "var(--fg-black)"

    return "color: RGB(" + contrast(colour, dark, bright) + ");"

"""
OnlyLegs filters
Custom Jinja2 filters
"""
from flask import Blueprint
from onlylegs.utils import colour as colour_utils
import colorsys


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


@blueprint.app_template_filter()
def hsl_hue(rgb):
    """
    Pass in a rgb value and will return the hue value
    """
    r, g, b = rgb
    r /= 255
    g /= 255
    b /= 255
    return colorsys.rgb_to_hls(r, g, b)[0] * 360


@blueprint.app_template_filter()
def hsl_saturation(rgb):
    """
    Pass in a rgb value and will return the saturation value
    """
    r, g, b = rgb
    r /= 255
    g /= 255
    b /= 255
    return colorsys.rgb_to_hls(r, g, b)[1] * 100

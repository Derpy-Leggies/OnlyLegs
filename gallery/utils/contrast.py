"""
Calculate the contrast between two colors
"""


def contrast(background, light, dark, threshold=0.179):
    """
    background: tuple of (r, g, b) values
    light: color to use if the background is light
    dark: color to use if the background is dark
    threshold: the threshold to use for determining lightness, the default is w3 recommended
    """
    red = background[0]
    green = background[1]
    blue = background[2]

    # Calculate contrast
    uicolors = [red / 255, green / 255, blue / 255]
    cont = [
        col / 12.92 if col <= 0.03928 else ((col + 0.055) / 1.055) ** 2.4
        for col in uicolors
    ]
    lightness = (0.2126 * cont[0]) + (0.7152 * cont[1]) + (0.0722 * cont[2])

    return light if lightness > threshold else dark

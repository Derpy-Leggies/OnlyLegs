def contrast(background, light, dark, threshold = 0.179):
    """
    Calculate the contrast between two colors
    background: tuple of (r, g, b) values
    light: color to use if the background is light
    dark: color to use if the background is dark
    threshold: the threshold to use for determining lightness, the default is w3 recommended
    """
    r = background[0]
    g = background[1]
    b = background[2]

    # Calculate contrast
    uicolors = [r / 255, g / 255, b / 255]
    c = [col / 12.92 if col <= 0.03928 else ((col + 0.055) / 1.055) ** 2.4 for col in uicolors]
    l = (0.2126 * c[0]) + (0.7152 * c[1]) + (0.0722 * c[2])
    
    return light if l > threshold else dark

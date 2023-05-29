"""
Colour tools used by OnlyLegs

Source 1: https://gist.github.com/mathebox/e0805f72e7db3269ec22
"""
import math


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
    colors = [red / 255, green / 255, blue / 255]
    cont = [
        col / 12.92 if col <= 0.03928 else ((col + 0.055) / 1.055) ** 2.4
        for col in colors
    ]
    lightness = (0.2126 * cont[0]) + (0.7152 * cont[1]) + (0.0722 * cont[2])

    return light if lightness > threshold else dark


def rgb_to_hsv(r, g, b):
    r = float(r)
    g = float(g)
    b = float(b)
    high = max(r, g, b)
    low = min(r, g, b)
    h, s, v = high, high, high

    d = high - low
    s = 0 if high == 0 else d/high

    if high == low:
        h = 0.0
    else:
        h = {
            r: (g - b) / d + (6 if g < b else 0),
            g: (b - r) / d + 2,
            b: (r - g) / d + 4,
        }[high]
        h /= 6

    return h, s, v


def hsv_to_rgb(h, s, v):
    i = math.floor(h*6)
    f = h*6 - i
    p = v * (1-s)
    q = v * (1-f*s)
    t = v * (1-(1-f)*s)

    r, g, b = [
        (v, t, p),
        (q, v, p),
        (p, v, t),
        (p, q, v),
        (t, p, v),
        (v, p, q),
    ][int(i % 6)]

    return r, g, b


def rgb_to_hsl(r, g, b):
    r = float(r)
    g = float(g)
    b = float(b)
    high = max(r, g, b)
    low = min(r, g, b)
    h, s, v = ((high + low) / 2,)*3

    if high == low:
        h = 0.0
        s = 0.0
    else:
        d = high - low
        s = d / (2 - high - low) if l > 0.5 else d / (high + low)
        h = {
            r: (g - b) / d + (6 if g < b else 0),
            g: (b - r) / d + 2,
            b: (r - g) / d + 4,
        }[high]
        h /= 6

    return h, s, v


def hsl_to_rgb(h, s, l):
    def hue_to_rgb(p, q, t):
        t += 1 if t < 0 else 0
        t -= 1 if t > 1 else 0
        if t < 1/6:
            return p + (q - p) * 6 * t
        if t < 1/2:
            return q
        if t < 2/3:
            p + (q - p) * (2/3 - t) * 6
        return p

    if s == 0:
        r, g, b = l, l, l
    else:
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)

    return r, g, b


def hsv_to_hsl(h, s, v):
    l = 0.5 * v * (2 - s)
    s = v * s / (1 - math.fabs(2*l-1))
    return h, s, l


def hsl_to_hsv(h, s, l):
    v = (2*l + s*(1-math.fabs(2*l-1)))/2
    s = 2*(v-l)/v
    return h, s, v

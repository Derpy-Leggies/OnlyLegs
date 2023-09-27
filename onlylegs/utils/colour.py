"""
Colour tools used by OnlyLegs

Source 1: https://gist.github.com/mathebox/e0805f72e7db3269ec22
"""


class Colour:
    def __init__(self, rgb):
        self.rgb = rgb

    def is_light(self, threshold=0.179):
        """
        returns True if background is light, False if dark
        threshold: the threshold to use for determining lightness, the default is w3 recommended
        """
        red, green, blue = self.rgb

        # Calculate contrast
        colors = [red / 255, green / 255, blue / 255]
        cont = [
            col / 12.92 if col <= 0.03928 else ((col + 0.055) / 1.055) ** 2.4
            for col in colors
        ]
        lightness = (0.2126 * cont[0]) + (0.7152 * cont[1]) + (0.0722 * cont[2])

        return lightness > threshold

    def to_hsv(self):
        r, g, b = self.rgb
        high = max(r, g, b)
        low = min(r, g, b)
        h, s, v = high, high, high

        d = high - low
        s = 0 if high == 0 else d / high

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

    def to_hsl(self):
        r, g, b = self.rgb
        high = max(r, g, b)
        low = min(r, g, b)
        h, s, v = ((high + low) / 2,) * 3

        if high == low:
            h = 0.0
            s = 0.0
        else:
            d = high - low
            s = d / (2 - high - low) if low > 0.5 else d / (high + low)
            h = {
                r: (g - b) / d + (6 if g < b else 0),
                g: (b - r) / d + 2,
                b: (r - g) / d + 4,
            }[high]
            h /= 6

        return h, s, v

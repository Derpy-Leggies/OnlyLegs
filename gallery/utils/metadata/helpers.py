"""
OnlyLegs - Metadata Parser
Metadata formatting helpers
"""
from datetime import datetime


def human_size(value):
    """
    Formats the size of a file in a human readable format
    """
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(value) < 1024.0:
            return f"{value:3.1f}{unit}B"
        value /= 1024.0

    return f"{value:.1f}YiB"


def date_format(value):
    """
    Formats the date into a standard format
    """
    return str(datetime.strptime(value, '%Y:%m:%d %H:%M:%S'))


def fnumber(value):
    """
    Formats the f-number into a standard format
    """
    return 'ƒ/' + str(value)


def iso(value):
    """
    Formats the ISO into a standard format
    """
    return 'ISO ' + str(value)


def shutter(value):
    """
    Formats the shutter speed into a standard format
    """
    return str(value) + 's'


def focal_length(value):
    """
    Formats the focal length into a standard format
    """
    try:
        return str(value[0] / value[1]) + 'mm'
    except TypeError:
        return str(value) + 'mm'


def exposure(value):
    """
    Formats the exposure value into a standard format
    """
    return str(value) + 'EV'


def color_space(value):
    """
    Maps the value of the color space to a human readable format
    """
    value_map = {
        0: 'Reserved',
        1: 'sRGB',
        65535: 'Uncalibrated'
    }
    try:
        return value_map[int(value)]
    except KeyError:
        return None


def flash(value):
    """
    Maps the value of the flash to a human readable format
    """
    value_map = {
        0: 'Flash did not fire',
        1: 'Flash fired',
        5: 'Strobe return light not detected',
        7: 'Strobe return light detected',
        9: 'Flash fired, compulsory flash mode',
        13: 'Flash fired, compulsory flash mode, return light not detected',
        15: 'Flash fired, compulsory flash mode, return light detected',
        16: 'Flash did not fire, compulsory flash mode',
        24: 'Flash did not fire, auto mode',
        25: 'Flash fired, auto mode',
        29: 'Flash fired, auto mode, return light not detected',
        31: 'Flash fired, auto mode, return light detected',
        32: 'No flash function',
        65: 'Flash fired, red-eye reduction mode',
        69: 'Flash fired, red-eye reduction mode, return light not detected',
        71: 'Flash fired, red-eye reduction mode, return light detected',
        73: 'Flash fired, compulsory flash mode, red-eye reduction mode',
        77: 'Flash fired, compulsory flash mode, red-eye reduction mode, return light not detected',
        79: 'Flash fired, compulsory flash mode, red-eye reduction mode, return light detected',
        89: 'Flash fired, auto mode, red-eye reduction mode',
        93: 'Flash fired, auto mode, return light not detected, red-eye reduction mode',
        95: 'Flash fired, auto mode, return light detected, red-eye reduction mode'
    }
    try:
        return value_map[int(value)]
    except KeyError:
        return None


def exposure_program(value):
    """
    Maps the value of the exposure program to a human readable format
    """
    value_map = {
        0: 'Not defined',
        1: 'Manual',
        2: 'Normal program',
        3: 'Aperture priority',
        4: 'Shutter priority',
        5: 'Creative program',
        6: 'Action program',
        7: 'Portrait mode',
        8: 'Landscape mode'
    }
    try:
        return value_map[int(value)]
    except KeyError:
        return None


def metering_mode(value):
    """
    Maps the value of the metering mode to a human readable format
    """
    value_map = {
        0: 'Unknown',
        1: 'Average',
        2: 'Center-Weighted Average',
        3: 'Spot',
        4: 'Multi-Spot',
        5: 'Pattern',
        6: 'Partial',
        255: 'Other'
    }
    try:
        return value_map[int(value)]
    except KeyError:
        return None


def resolution_unit(value):
    """
    Maps the value of the resolution unit to a human readable format
    """
    value_map = {
        1: 'No absolute unit of measurement',
        2: 'Inch',
        3: 'Centimeter'
    }
    try:
        return value_map[int(value)]
    except KeyError:
        return None


def light_source(value):
    """
    Maps the value of the light source to a human readable format
    """
    value_map = {
        0: 'Unknown',
        1: 'Daylight',
        2: 'Fluorescent',
        3: 'Tungsten (incandescent light)',
        4: 'Flash',
        9: 'Fine weather',
        10: 'Cloudy weather',
        11: 'Shade',
        12: 'Daylight fluorescent (D 5700 - 7100K)',
        13: 'Day white fluorescent (N 4600 - 5400K)',
        14: 'Cool white fluorescent (W 3900 - 4500K)',
        15: 'White fluorescent (WW 3200 - 3700K)',
        17: 'Standard light A',
        18: 'Standard light B',
        19: 'Standard light C',
        20: 'D55',
        21: 'D65',
        22: 'D75',
        23: 'D50',
        24: 'ISO studio tungsten',
        255: 'Other light source',
    }
    try:
        return value_map[int(value)]
    except KeyError:
        return None


def scene_capture_type(value):
    """
    Maps the value of the scene capture type to a human readable format
    """
    value_map = {
        0: 'Standard',
        1: 'Landscape',
        2: 'Portrait',
        3: 'Night scene',
    }
    try:
        return value_map[int(value)]
    except KeyError:
        return None


def white_balance(value):
    """
    Maps the value of the white balance to a human readable format
    """
    value_map = {
        0: 'Auto white balance',
        1: 'Manual white balance',
    }
    try:
        return value_map[int(value)]
    except KeyError:
        return None


def exposure_mode(value):
    """
    Maps the value of the exposure mode to a human readable format
    """
    value_map = {
        0: 'Auto exposure',
        1: 'Manual exposure',
        2: 'Auto bracket',
    }
    try:
        return value_map[int(value)]
    except KeyError:
        return None


def sensitivity_type(value):
    """
    Maps the value of the sensitivity type to a human readable format
    """
    value_map = {
        0:
        'Unknown',
        1:
        'Standard Output Sensitivity',
        2:
        'Recommended Exposure Index',
        3:
        'ISO Speed',
        4:
        'Standard Output Sensitivity and Recommended Exposure Index',
        5:
        'Standard Output Sensitivity and ISO Speed',
        6:
        'Recommended Exposure Index and ISO Speed',
        7:
        'Standard Output Sensitivity, Recommended Exposure Index and ISO Speed',
    }
    try:
        return value_map[int(value)]
    except KeyError:
        return None


def lens_specification(value):
    """
    Maps the value of the lens specification to a human readable format
    """
    try:
        return str(value[0] / value[1]) + 'mm - ' + str(value[2] / value[3]) + 'mm'
    except TypeError:
        return None


def compression_type(value):
    """
    Maps the value of the compression type to a human readable format
    """
    value_map = {
        1: 'Uncompressed',
        2: 'CCITT 1D',
        3: 'T4/Group 3 Fax',
        4: 'T6/Group 4 Fax',
        5: 'LZW',
        6: 'JPEG (old-style)',
        7: 'JPEG',
        8: 'Adobe Deflate',
        9: 'JBIG B&W',
        10: 'JBIG Color',
        99: 'JPEG',
        262: 'Kodak 262',
        32766: 'Next',
        32767: 'Sony ARW Compressed',
        32769: 'Packed RAW',
        32770: 'Samsung SRW Compressed',
        32771: 'CCIRLEW',
        32772: 'Samsung SRW Compressed 2',
        32773: 'PackBits',
        32809: 'Thunderscan',
        32867: 'Kodak KDC Compressed',
        32895: 'IT8CTPAD',
        32896: 'IT8LW',
        32897: 'IT8MP',
        32898: 'IT8BL',
        32908: 'PixarFilm',
        32909: 'PixarLog',
        32946: 'Deflate',
        32947: 'DCS',
        33003: 'Aperio JPEG 2000 YCbCr',
        33005: 'Aperio JPEG 2000 RGB',
        34661: 'JBIG',
        34676: 'SGILog',
        34677: 'SGILog24',
        34712: 'JPEG 2000',
        34713: 'Nikon NEF Compressed',
        34715: 'JBIG2 TIFF FX',
        34718: '(MDI) Binary Level Codec',
        34719: '(MDI) Progressive Transform Codec',
        34720: '(MDI) Vector',
        34887: 'ESRI Lerc',
        34892: 'Lossy JPEG',
        34925: 'LZMA2',
        34926: 'Zstd',
        34927: 'WebP',
        34933: 'PNG',
        34934: 'JPEG XR',
        65000: 'Kodak DCR Compressed',
        65535: 'Pentax PEF Compressed',
    }
    try:
        return value_map[int(value)]
    except KeyError:
        return None


def orientation(value):
    """
    Maps the value of the orientation to a human readable format
    """
    value_map = {
        0: 'Undefined',
        1: 'Horizontal (normal)',
        2: 'Mirror horizontal',
        3: 'Rotate 180',
        4: 'Mirror vertical',
        5: 'Mirror horizontal and rotate 270 CW',
        6: 'Rotate 90 CW',
        7: 'Mirror horizontal and rotate 90 CW',
        8: 'Rotate 270 CW',
    }
    try:
        return value_map[int(value)]
    except KeyError:
        return None


def components_configuration(value):
    """
    Maps the value of the components configuration to a human readable format
    """
    value_map = {
        0: '',
        1: 'Y',
        2: 'Cb',
        3: 'Cr',
        4: 'R',
        5: 'G',
        6: 'B',
    }
    try:
        return ''.join([value_map[int(x)] for x in value])
    except KeyError:
        return None


def rating(value):
    """
    Maps the value of the rating to a human readable format
    """
    return str(value) + ' stars'


def rating_percent(value):
    """
    Maps the value of the rating to a human readable format
    """
    return str(value) + '%'


def pixel_dimension(value):
    """
    Maps the value of the pixel dimension to a human readable format
    """
    return str(value) + 'px'

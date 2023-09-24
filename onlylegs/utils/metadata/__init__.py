"""
OnlyLegs - Metadata Parser
Parse metadata from images if available
otherwise get some basic information from the file
"""
import os

from PIL import Image
from PIL.ExifTags import TAGS

from .helpers import *
from .mapping import *


def yoink(file_path):
    """
    Initialize the metadata parser
    """
    if not os.path.isfile(file_path):
        return None

    img_exif = {}
    file = Image.open(file_path)

    img_exif["FileName"] = os.path.basename(file_path)
    img_exif["FileSize"] = os.path.getsize(file_path)
    img_exif["FileFormat"] = img_exif["FileName"].split(".")[-1]
    img_exif["FileWidth"], img_exif["FileHeight"] = file.size

    try:
        tags = file._getexif()
        for tag, value in TAGS.items():
            if tag in tags:
                img_exif[value] = tags[tag]
    except TypeError:
        pass

    file.close()

    return _format_data(img_exif)


def _format_data(encoded):
    """
    Formats the data into a dictionary
    """
    exif = {
        "Photographer": {},
        "Camera": {},
        "Software": {},
        "File": {},
    }

    # Thanks chatGPT xP
    # the helper function works, so not sure why it triggers pylint
    for key, value in encoded.items():
        for mapping_name, mapping_val in EXIF_MAPPING:
            if key in mapping_val:
                if len(mapping_val[key]) == 2:
                    exif[mapping_name][mapping_val[key][0]] = {
                        "raw": value,
                        "formatted": (
                            getattr(
                                helpers,  # pylint: disable=E0602
                                mapping_val[key][1],
                            )(value)
                        ),
                    }
                else:
                    exif[mapping_name][mapping_val[key][0]] = {
                        "raw": value,
                    }
                continue

    # Remove empty keys
    if not exif["Photographer"]:
        del exif["Photographer"]
    if not exif["Camera"]:
        del exif["Camera"]
    if not exif["Software"]:
        del exif["Software"]
    if not exif["File"]:
        del exif["File"]

    return exif

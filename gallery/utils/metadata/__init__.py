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


class Metadata:
    """
    Metadata parser
    """
    def __init__(self, file_path):
        """
        Initialize the metadata parser
        """
        self.file_path = file_path
        img_exif = {}

        try:
            file = Image.open(file_path)
            tags = file._getexif()
            img_exif = {}

            for tag, value in TAGS.items():
                if tag in tags:
                    img_exif[value] = tags[tag]

            img_exif['FileName'] = os.path.basename(file_path)
            img_exif['FileSize'] = os.path.getsize(file_path)
            img_exif['FileFormat'] = img_exif['FileName'].split('.')[-1]
            img_exif['FileWidth'], img_exif['FileHeight'] = file.size

            file.close()
        except TypeError:
            img_exif['FileName'] = os.path.basename(file_path)
            img_exif['FileSize'] = os.path.getsize(file_path)
            img_exif['FileFormat'] = img_exif['FileName'].split('.')[-1]
            img_exif['FileWidth'], img_exif['FileHeight'] = file.size

        self.encoded = img_exif

    def yoink(self):
        """
        Yoinks the metadata from the image
        """
        if not os.path.isfile(self.file_path):
            return None
        return self.format_data(self.encoded)

    @staticmethod
    def format_data(encoded_exif):
        """
        Formats the data into a dictionary
        """
        exif = {
            'Photographer': {},
            'Camera': {},
            'Software': {},
            'File': {},
        }

        # Thanks chatGPT xP
        for key, value in encoded_exif.items():
            for mapping_name, mapping_val in EXIF_MAPPING:
                if key in mapping_val:
                    if len(mapping_val[key]) == 2:
                        exif[mapping_name][mapping_val[key][0]] = {
                            'raw': value,
                            'formatted': getattr(helpers, mapping_val[key][1])(value),  # pylint: disable=E0602
                        }
                    else:
                        exif[mapping_name][mapping_val[key][0]] = {
                            'raw': value,
                        }
                    continue

        # Remove empty keys
        if not exif['Photographer']:
            del exif['Photographer']
        if not exif['Camera']:
            del exif['Camera']
        if not exif['Software']:
            del exif['Software']
        if not exif['File']:
            del exif['File']

        return exif

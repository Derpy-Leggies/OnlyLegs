"""
OnlyLegs - Metatada Parser
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

    def format_data(self, encoded_exif): # pylint: disable=R0912 # For now, this is fine
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
            for mapping_name, mapping in EXIF_MAPPING:
                if key in mapping:
                    if len(mapping[key]) == 2:
                        exif[mapping_name][mapping[key][0]] = {
                            'raw': value,
                            'formatted': getattr(helpers, mapping[key][1])(value),
                        }
                    else:
                        exif[mapping_name][mapping[key][0]] = {
                            'raw': value,
                        }

        # Remove empty keys
        if len(exif['Photographer']) == 0:
            del exif['Photographer']
        if len(exif['Camera']) == 0:
            del exif['Camera']
        if len(exif['Software']) == 0:
            del exif['Software']
        if len(exif['File']) == 0:
            del exif['File']

        return exif

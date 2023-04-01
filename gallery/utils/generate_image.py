"""
Tools for generating images and thumbnails
"""

import os
import platformdirs
from PIL import Image, ImageOps  #, ImageFilter
from werkzeug.utils import secure_filename


CACHE_PATH = platformdirs.user_config_dir('onlylegs') + '/cache'
UPLOAD_PATH = platformdirs.user_config_dir('onlylegs') + '/uploads'


def generate_thumbnail(file_name, resolution, ext=None):
    """
    Image thumbnail generator
    Uses PIL to generate a thumbnail of the image and saves it to the cache directory
    Name is the filename
    resolution: 400x400 or thumb, or any other resolution
    ext is the file extension of the image
    """
    # Make image cache directory if it doesn't exist
    if not os.path.exists(CACHE_PATH):
        os.makedirs(CACHE_PATH)

    # no sussy business
    file_name, file_ext = secure_filename(file_name).rsplit('.')
    if not ext:
        ext = file_ext.strip('.')

    # PIL doesnt like jpg so we convert it to jpeg
    if ext.lower() == "jpg":
        ext = "jpeg"

    # Set resolution based on preset resolutions
    if resolution in ['prev', 'preview']:
        res_x, res_y = (1920, 1080)
    elif resolution in ['thumb', 'thumbnail']:
        res_x, res_y = (400, 400)
    elif resolution in ['icon', 'favicon']:
        res_x, res_y = (10, 10)
    elif len(resolution.split('x')) == 2:
        res_x, res_y = resolution.split('x')
    else:
        return None

    # If image has been already generated, return it from the cache
    if os.path.exists(os.path.join(CACHE_PATH, f'{file_name}_{res_x}x{res_y}.{ext}')):
        return os.path.join(CACHE_PATH, f'{file_name}_{res_x}x{res_y}.{ext}')

    # Check if image exists in the uploads directory
    if not os.path.exists(os.path.join(UPLOAD_PATH, f'{file_name}.{file_ext}')):
        return None

    # Open image and rotate it based on EXIF data and get ICC profile so colors are correct
    image = Image.open(os.path.join(UPLOAD_PATH, f'{file_name}.{file_ext}'))
    image_icc = image.info.get("icc_profile")
    img_x, img_y = image.size

    # Resize image to fit the resolution
    image = ImageOps.exif_transpose(image)
    image.thumbnail((min(img_x, int(res_x)), min(img_y, int(res_y))), Image.ANTIALIAS)

    # Save image to cache directory
    try:
        image.save(os.path.join(CACHE_PATH,f'{file_name}_{res_x}x{res_y}.{ext}'),
                    icc_profile=image_icc)
    except OSError:
        # This usually happens when saving a JPEG with an ICC profile,
        # so we convert to RGB and try again
        image = image.convert('RGB')
        image.save(os.path.join(CACHE_PATH, f'{file_name}_{res_x}x{res_y}.{ext}'),
                    icc_profile=image_icc)

    # No need to keep the image in memory, learned the hard way
    image.close()

    return os.path.join(CACHE_PATH, f'{file_name}_{res_x}x{res_y}.{ext}')

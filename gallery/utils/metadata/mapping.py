"""
OnlyLegs - Metatada Parser
Mapping for metadata
"""

PHOTOGRAHER_MAPPING = {
    "Artist": ["Artist"],
    "UserComment": ["Comment"],
    "ImageDescription": ["Description"],
    "Copyright": ["Copyright"],
}
CAMERA_MAPPING = {
    "Model": ["Model", "title"],
    "Make": ["Manifacturer", "title"],
    "BodySerialNumber": ["Camera Type"],
    "LensMake": ["Lens Make", "title"],
    "LensModel": ["Lens Model", "title"],
    "LensSpecification": ["Lens Specification", "lens_specification"],
    "ComponentsConfiguration": ["Components Configuration", "components_configuration"],
    "DateTime": ["Date and Time", "date_format"],
    "DateTimeOriginal": ["Date and Time (Original)", "date_format"],
    "DateTimeDigitized": ["Date and Time (Digitized)", "date_format"],
    "OffsetTime": ["Time Offset"],
    "OffsetTimeOriginal": ["Time Offset (Original)"],
    "OffsetTimeDigitized": ["Time Offset (Digitized)"],
    "FNumber": ["FNumber", "fnumber"],
    "FocalLength": ["Focal Length", "focal_length"],
    "FocalLengthIn35mmFilm": ["Focal Length in 35mm format", "focal_length"],
    "MaxApertureValue": ["Max Aperture", "fnumber"],
    "ApertureValue": ["Aperture", "fnumber"],
    "ShutterSpeedValue": ["Shutter Speed", "shutter"],
    "ISOSpeedRatings": ["ISO Speed Ratings", "iso"],
    "ISOSpeed": ["ISO Speed", "iso"],
    "SensitivityType": ["Sensitivity Type", "sensitivity_type"],
    "ExposureBiasValue": ["Exposure Bias", "exposure"],
    "ExposureTime": ["Exposure Time", "shutter"],
    "ExposureMode": ["Exposure Mode", "exposure_mode"],
    "ExposureProgram": ["Exposure Program", "exposure_program"],
    "WhiteBalance": ["White Balance", "white_balance"],
    "Flash": ["Flash", "flash"],
    "MeteringMode": ["Metering Mode", "metering_mode"],
    "LightSource": ["Light Source", "light_source"],
    "SceneCaptureType": ["Scene Capture Type", "scene_capture_type"],
    "SubjectDistance": ["Subject Distance", "subject_distance"],
    "SubjectDistanceRange": ["Subject Distance Range", "subject_distance_range"],
}
SOFTWARE_MAPPING = {
    "Software": ["Software"],
    "ColorSpace": ["Colour Space", "color_space"],
    "Compression": ["Compression", "compression_type"],
}
FILE_MAPPING = {
    "FileName": ["Name"],
    "FileSize": ["Size", "human_size"],
    "FileFormat": ["Format"],
    "FileWidth": ["Width", "pixel_dimension"],
    "FileHeight": ["Height", "pixel_dimension"],
    "Orientation": ["Orientation", "orientation"],
    "XResolution": ["X-resolution"],
    "YResolution": ["Y-resolution"],
    "ResolutionUnit": ["Resolution Units", "resolution_unit"],
    "Rating": ["Rating", "rating"],
    "RatingPercent": ["Rating Percent", "rating_percent"],
}

EXIF_MAPPING = [
    ("Photographer", PHOTOGRAHER_MAPPING),
    ("Camera", CAMERA_MAPPING),
    ("Software", SOFTWARE_MAPPING),
    ("File", FILE_MAPPING),
]

import PIL
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime
import os


class metadata:

    def yoink(filename):
        exif = metadata.getFile(filename)
        file_size = os.path.getsize(filename)
        file_name = os.path.basename(filename)
        file_resolution = Image.open(filename).size

        if exif:
            unformatted_exif = metadata.format(exif, file_size, file_name,
                                               file_resolution)
        else:
            # No EXIF data, get some basic informaton from the file
            unformatted_exif = {
                'File': {
                    'Name': {
                        'type': 'text',
                        'raw': file_name
                    },
                    'Size': {
                        'type': 'number',
                        'raw': file_size,
                        'formatted': metadata.human_size(file_size)
                    },
                    'Format': {
                        'type': 'text',
                        'raw': file_name.split('.')[-1]
                    },
                    'Width': {
                        'type': 'number',
                        'raw': file_resolution[0]
                    },
                    'Height': {
                        'type': 'number',
                        'raw': file_resolution[1]
                    },
                }
            }

        formatted_exif = {}

        for section in unformatted_exif:
            tmp = {}

            for value in unformatted_exif[section]:
                if unformatted_exif[section][value]['raw'] != None:
                    raw_type = unformatted_exif[section][value]['raw']
                    if isinstance(raw_type, PIL.TiffImagePlugin.IFDRational):
                        raw_type = raw_type.__float__()
                    elif isinstance(raw_type, bytes):
                        raw_type = raw_type.decode('utf-8')

                    tmp[value] = unformatted_exif[section][value]

            if len(tmp) > 0:
                formatted_exif[section] = tmp

        return formatted_exif

    def getFile(filename):
        try:
            file = Image.open(filename)
            raw = file._getexif()
            exif = {}

            for tag, value in TAGS.items():

                if tag in raw:
                    data = raw[tag]
                else:
                    data = None

                exif[value] = {"tag": tag, "raw": data}

            file.close()

            return exif
        except Exception as e:
            return False

    def format(raw, file_size, file_name, file_resolution):
        exif = {}

        exif['Photographer'] = {
            'Artist': {
                'type': 'text',
                'raw': raw["Artist"]["raw"]
            },
            'Comment': {
                'type': 'text',
                'raw': raw["UserComment"]["raw"]
            },
            'Description': {
                'type': 'text',
                'raw': raw["ImageDescription"]["raw"]
            },
            'Copyright': {
                'type': 'text',
                'raw': raw["Copyright"]["raw"]
            },
        }
        exif['Camera'] = {
            'Model': {
                'type': 'text',
                'raw': raw['Model']['raw']
            },
            'Make': {
                'type': 'text',
                'raw': raw['Make']['raw']
            },
            'Camera Type': {
                'type': 'text',
                'raw': raw['BodySerialNumber']['raw']
            },
            'Lens Make': {
                'type': 'text',
                'raw': raw['LensMake']['raw'],
            },
            'Lense Model': {
                'type': 'text',
                'raw': raw['LensModel']['raw'],
            },
            'Lense Spec': {
                'type':
                'text',
                'raw':
                raw['LensSpecification']['raw'],
                'formatted':
                metadata.lensSpecification(raw['LensSpecification']['raw'])
            },
            'Component Config': {
                'type':
                'text',
                'raw':
                raw['ComponentsConfiguration']['raw'],
                'formatted':
                metadata.componentsConfiguration(
                    raw['ComponentsConfiguration']['raw'])
            },
            'Date Processed': {
                'type': 'date',
                'raw': raw['DateTime']['raw'],
                'formatted': metadata.date(raw['DateTime']['raw'])
            },
            'Date Digitized': {
                'type': 'date',
                'raw': raw["DateTimeDigitized"]["raw"],
                'formatted': metadata.date(raw["DateTimeDigitized"]["raw"])
            },
            'Time Offset': {
                'type': 'text',
                'raw': raw["OffsetTime"]["raw"]
            },
            'Time Offset - Original': {
                'type': 'text',
                'raw': raw["OffsetTimeOriginal"]["raw"]
            },
            'Time Offset - Digitized': {
                'type': 'text',
                'raw': raw["OffsetTimeDigitized"]["raw"]
            },
            'Date Original': {
                'type': 'date',
                'raw': raw["DateTimeOriginal"]["raw"],
                'formatted': metadata.date(raw["DateTimeOriginal"]["raw"])
            },
            'FNumber': {
                'type': 'fnumber',
                'raw': raw["FNumber"]["raw"],
                'formatted': metadata.fnumber(raw["FNumber"]["raw"])
            },
            'Focal Length': {
                'type': 'focal',
                'raw': raw["FocalLength"]["raw"],
                'formatted': metadata.focal(raw["FocalLength"]["raw"])
            },
            'Focal Length (35mm format)': {
                'type': 'focal',
                'raw': raw["FocalLengthIn35mmFilm"]["raw"],
                'formatted':
                metadata.focal(raw["FocalLengthIn35mmFilm"]["raw"])
            },
            'Max Aperture': {
                'type': 'fnumber',
                'raw': raw["MaxApertureValue"]["raw"],
                'formatted': metadata.fnumber(raw["MaxApertureValue"]["raw"])
            },
            'Aperture': {
                'type': 'fnumber',
                'raw': raw["ApertureValue"]["raw"],
                'formatted': metadata.fnumber(raw["ApertureValue"]["raw"])
            },
            'Shutter Speed': {
                'type': 'shutter',
                'raw': raw["ShutterSpeedValue"]["raw"],
                'formatted': metadata.shutter(raw["ShutterSpeedValue"]["raw"])
            },
            'ISO Speed Ratings': {
                'type': 'number',
                'raw': raw["ISOSpeedRatings"]["raw"],
                'formatted': metadata.iso(raw["ISOSpeedRatings"]["raw"])
            },
            'ISO Speed': {
                'type': 'iso',
                'raw': raw["ISOSpeed"]["raw"],
                'formatted': metadata.iso(raw["ISOSpeed"]["raw"])
            },
            'Sensitivity Type': {
                'type':
                'number',
                'raw':
                raw["SensitivityType"]["raw"],
                'formatted':
                metadata.sensitivityType(raw["SensitivityType"]["raw"])
            },
            'Exposure Bias': {
                'type': 'ev',
                'raw': raw["ExposureBiasValue"]["raw"],
                'formatted': metadata.ev(raw["ExposureBiasValue"]["raw"])
            },
            'Exposure Time': {
                'type': 'shutter',
                'raw': raw["ExposureTime"]["raw"],
                'formatted': metadata.shutter(raw["ExposureTime"]["raw"])
            },
            'Exposure Mode': {
                'type': 'number',
                'raw': raw["ExposureMode"]["raw"],
                'formatted': metadata.exposureMode(raw["ExposureMode"]["raw"])
            },
            'Exposure Program': {
                'type':
                'number',
                'raw':
                raw["ExposureProgram"]["raw"],
                'formatted':
                metadata.exposureProgram(raw["ExposureProgram"]["raw"])
            },
            'White Balance': {
                'type': 'number',
                'raw': raw["WhiteBalance"]["raw"],
                'formatted': metadata.whiteBalance(raw["WhiteBalance"]["raw"])
            },
            'Flash': {
                'type': 'number',
                'raw': raw["Flash"]["raw"],
                'formatted': metadata.flash(raw["Flash"]["raw"])
            },
            'Metering Mode': {
                'type': 'number',
                'raw': raw["MeteringMode"]["raw"],
                'formatted': metadata.meteringMode(raw["MeteringMode"]["raw"])
            },
            'Light Source': {
                'type': 'number',
                'raw': raw["LightSource"]["raw"],
                'formatted': metadata.lightSource(raw["LightSource"]["raw"])
            },
            'Scene Capture Type': {
                'type':
                'number',
                'raw':
                raw["SceneCaptureType"]["raw"],
                'formatted':
                metadata.sceneCaptureType(raw["SceneCaptureType"]["raw"])
            },
            'Scene Type': {
                'type': 'number',
                'raw': raw["SceneType"]["raw"],
                'formatted': metadata.sceneType(raw["SceneType"]["raw"])
            },
            'Rating': {
                'type': 'number',
                'raw': raw["Rating"]["raw"],
                'formatted': metadata.rating(raw["Rating"]["raw"])
            },
            'Rating Percent': {
                'type': 'number',
                'raw': raw["RatingPercent"]["raw"],
                'formatted':
                metadata.ratingPercent(raw["RatingPercent"]["raw"])
            },
        }
        exif['Software'] = {
            'Software': {
                'type': 'text',
                'raw': raw['Software']['raw']
            },
            'Colour Space': {
                'type': 'number',
                'raw': raw['ColorSpace']['raw'],
                'formatted': metadata.colorSpace(raw['ColorSpace']['raw'])
            },
            'Compression': {
                'type': 'number',
                'raw': raw['Compression']['raw'],
                'formatted': metadata.compression(raw['Compression']['raw'])
            },
        }
        exif['File'] = {
            'Name': {
                'type': 'text',
                'raw': file_name
            },
            'Size': {
                'type': 'number',
                'raw': file_size,
                'formatted': metadata.human_size(file_size)
            },
            'Format': {
                'type': 'text',
                'raw': file_name.split('.')[-1]
            },
            'Width': {
                'type': 'number',
                'raw': file_resolution[0]
            },
            'Height': {
                'type': 'number',
                'raw': file_resolution[1]
            },
            'Orientation': {
                'type': 'number',
                'raw': raw["Orientation"]["raw"],
                'formatted': metadata.orientation(raw["Orientation"]["raw"])
            },
            'Xresolution': {
                'type': 'number',
                'raw': raw["XResolution"]["raw"]
            },
            'Yresolution': {
                'type': 'number',
                'raw': raw["YResolution"]["raw"]
            },
            'Resolution Units': {
                'type': 'number',
                'raw': raw["ResolutionUnit"]["raw"],
                'formatted':
                metadata.resolutionUnit(raw["ResolutionUnit"]["raw"])
            },
        }
        #exif['Raw'] = {}
        #for key in raw:
        #    try:
        #        exif['Raw'][key] = {
        #            'type': 'text',
        #            'raw': raw[key]['raw'].decode('utf-8')
        #        }
        #    except:
        #        exif['Raw'][key] = {
        #            'type': 'text',
        #            'raw': str(raw[key]['raw'])
        #        }

        return exif

    def human_size(num, suffix="B"):
        for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
            if abs(num) < 1024.0:
                return f"{num:3.1f}{unit}{suffix}"
            num /= 1024.0
        return f"{num:.1f}Yi{suffix}"

    def date(date):
        date_format = '%Y:%m:%d %H:%M:%S'

        if date:
            return str(datetime.strptime(date, date_format))
        else:
            return None

    def fnumber(value):
        if value != None:
            return 'f/' + str(value)
        else:
            return None

    def iso(value):
        if value != None:
            return 'ISO ' + str(value)
        else:
            return None

    def shutter(value):
        if value != None:
            return str(value) + 's'
        else:
            return None

    def focal(value):
        if value != None:
            try:
                return str(value[0] / value[1]) + 'mm'
            except:
                return str(value) + 'mm'
        else:
            return None

    def ev(value):
        if value != None:
            return str(value) + 'EV'
        else:
            return None

    def colorSpace(value):
        types = {1: 'sRGB', 65535: 'Uncalibrated', 0: 'Reserved'}
        try:
            return types[int(value)]
        except:
            return None

    def flash(value):
        types = {
            0:
            'Flash did not fire',
            1:
            'Flash fired',
            5:
            'Strobe return light not detected',
            7:
            'Strobe return light detected',
            9:
            'Flash fired, compulsory flash mode',
            13:
            'Flash fired, compulsory flash mode, return light not detected',
            15:
            'Flash fired, compulsory flash mode, return light detected',
            16:
            'Flash did not fire, compulsory flash mode',
            24:
            'Flash did not fire, auto mode',
            25:
            'Flash fired, auto mode',
            29:
            'Flash fired, auto mode, return light not detected',
            31:
            'Flash fired, auto mode, return light detected',
            32:
            'No flash function',
            65:
            'Flash fired, red-eye reduction mode',
            69:
            'Flash fired, red-eye reduction mode, return light not detected',
            71:
            'Flash fired, red-eye reduction mode, return light detected',
            73:
            'Flash fired, compulsory flash mode, red-eye reduction mode',
            77:
            'Flash fired, compulsory flash mode, red-eye reduction mode, return light not detected',
            79:
            'Flash fired, compulsory flash mode, red-eye reduction mode, return light detected',
            89:
            'Flash fired, auto mode, red-eye reduction mode',
            93:
            'Flash fired, auto mode, return light not detected, red-eye reduction mode',
            95:
            'Flash fired, auto mode, return light detected, red-eye reduction mode'
        }
        try:
            return types[int(value)]
        except:
            return None

    def exposureProgram(value):
        types = {
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
            return types[int(value)]
        except:
            return None

    def meteringMode(value):
        types = {
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
            return types[int(value)]
        except:
            return None

    def resolutionUnit(value):
        types = {
            1: 'No absolute unit of measurement',
            2: 'Inch',
            3: 'Centimeter'
        }
        try:
            return types[int(value)]
        except:
            return None

    def lightSource(value):
        types = {
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
            return types[int(value)]
        except:
            return None

    def sceneCaptureType(value):
        types = {
            0: 'Standard',
            1: 'Landscape',
            2: 'Portrait',
            3: 'Night scene',
        }
        try:
            return types[int(value)]
        except:
            return None

    def sceneType(value):
        if value:
            return 'Directly photographed image'
        else:
            return None

    def whiteBalance(value):
        types = {
            0: 'Auto white balance',
            1: 'Manual white balance',
        }
        try:
            return types[int(value)]
        except:
            return None

    def exposureMode(value):
        types = {
            0: 'Auto exposure',
            1: 'Manual exposure',
            2: 'Auto bracket',
        }
        try:
            return types[int(value)]
        except:
            return None

    def sensitivityType(value):
        types = {
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
            return types[int(value)]
        except:
            return None

    def lensSpecification(value):
        if value:
            return str(value[0] / value[1]) + 'mm - ' + str(
                value[2] / value[3]) + 'mm'
        else:
            return None

    def compression(value):
        types = {
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
            return types[int(value)]
        except:
            return None

    def orientation(value):
        types = {
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
            return types[int(value)]
        except:
            return None

    def componentsConfiguration(value):
        types = {
            0: '',
            1: 'Y',
            2: 'Cb',
            3: 'Cr',
            4: 'R',
            5: 'G',
            6: 'B',
        }
        try:
            return ''.join([types[int(x)] for x in value])
        except:
            return None

    def rating(value):
        return str(value) + ' stars'

    def ratingPercent(value):
        return str(value) + '%'
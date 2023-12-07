""" This module deals with datasets from the prostgersql database"""

def get_rgb_filenames(myds):

    rgb = []
    rgb.append(myds.measurements['red']['path'])
    rgb.append(myds.measurements['green']['path'])
    rgb.append(myds.measurements['blue']['path'])

    return rgb

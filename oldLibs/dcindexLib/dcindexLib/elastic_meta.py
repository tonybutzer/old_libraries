
"""
odc-little-cube

use elatic instead of postgresql -

1. less code
2. more cloud-native

"""

#import logging
import sys
import os
#import json
#import pprint

from collections import OrderedDict

#from dcindexLib.xml_meta_lib import get_metadata_docs_bucket   # uses xml based metadata
from dcindexLib.parse_json import get_metadata_docs_json

from dcindexLib.projection_stuff import get_projection_info
# from dcindexLib.elastic_index import connect_elasticsearch
# from dcindexLib.elastic_index import l_create_index
# from dcindexLib.elastic_index import store_record


def create_footprint(coord):

    # still need to figure out if its lon,lat or lat,lon
    # in most cases the routines are now longitude the latitude or (x then y)
    print("TONY foot coord:", coord)

    foot = {
                "type": "Polygon", 
                "coordinates": [
                    [
                        [
                            float(coord['ul']['lon']),
                            float(coord['ul']['lat'])
                        ], 
                        [
                            float(coord['ur']['lon']),
                            float(coord['ur']['lat'])
                        ], 
                        [
                            float(coord['lr']['lon']),
                            float(coord['lr']['lat'])
                        ], 
                        [
                            float(coord['ll']['lon']),
                            float(coord['ll']['lat'])
                        ],
                        [
                            float(coord['ul']['lon']),
                            float(coord['ul']['lat'])
                        ] 
                    ]
                ]

    } 

    print (foot)

    return foot

def elastic_flatten_doc(mdoc):
    foot = create_footprint(mdoc['extent']['coord'])
    elastic_doc = {
                    'creation_dt': mdoc['creation_dt'],
                    'processing_level': mdoc['processing_level'],
                    'red': mdoc['image']['bands']['red']['path'],
                    'green': mdoc['image']['bands']['green']['path'],
                    'blue': mdoc['image']['bands']['blue']['path'],
                    'nir': mdoc['image']['bands']['nir']['path'],
                    'pixel_qa': mdoc['image']['bands']['pixel_qa']['path'],
                    'ul': {
                            'lat': mdoc['extent']['coord']['ul']['lat'],
                            'lon': mdoc['extent']['coord']['ul']['lon'],
                        },
                    'footprint': foot
                }
    return elastic_doc




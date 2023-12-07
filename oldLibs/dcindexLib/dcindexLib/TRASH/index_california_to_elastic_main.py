
"""
odc-little-cube

use elatic instead of postgresql -

1. less code
2. more cloud-native

"""

import logging
import sys
import os
import json
import pprint

from collections import OrderedDict

# from dcindexLib.xml_meta_lib import get_metadata_docs_bucket
from dcindexLib.json_meta_lib import get_metadata_docs_json

from dcindexLib.projection_stuff import get_projection_info
from dcindexLib.elastic_index import connect_elasticsearch
from dcindexLib.elastic_index import create_index
from dcindexLib.elastic_index import store_record


def create_footprint(coord):
    print("TONY foot coord:", coord)
    foot = {
                "type": "Polygon", 
                "coordinates": [
                    [
                        [
                            float(coord['ul']['lat']),
                            float(coord['ul']['lon'])
                        ], 
                        [
                            float(coord['ur']['lat']),
                            float(coord['ur']['lon'])
                        ], 
                        [
                            float(coord['lr']['lat']),
                            float(coord['lr']['lon'])
                        ], 
                        [
                            float(coord['ll']['lat']),
                            float(coord['ll']['lon'])
                        ],
                        [
                            float(coord['ul']['lat']),
                            float(coord['ul']['lon'])
                        ] 
                    ]
                ]
    } 
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



def elastic_all_metatdata(bucket, top_directory_prefix):
    """ Main loop function to traverse/crawl the bucket-->prefix or filesystem directory tree and index each dataset

    for each .json metadata file:

    * extract the metadata and 
    * create a doc (dict json blob for the postgresql database)

    Args:
        **bucket_name** (str): AWS S3 Bucket Name - example lsaa-staging-cog

        config (str): A datacube config file to over-ride the one in your home directory

        **prefix** (str): AWS prefix within the bucket to start the recursive search for .json file = example L8

    Returns:
        ABSOLUTELY_NOTHING

    """
    print ("meta loop")
    cnt=0;

    es_conn = connect_elasticsearch()


    # delete any old indexes - similar to clearing the postgres db
    es_conn.indices.delete(index='datacube', ignore=[400, 404])

    # create new elastic search index
    create_index(es_conn, index_name='datacube')

    for metadata_path, metadata_doc in get_metadata_docs_json(bucket, top_directory_prefix):
        uri = metadata_path
        print(uri)
        cnt=cnt+1
        print(cnt)
        print("META:", metadata_doc)
        elastic_ready_doc = elastic_flatten_doc(metadata_doc)
        # add_dataset(metadata_doc, uri, rules, index)
        logging.info("Indexing %s", metadata_path)
        print("creationdate", metadata_doc['creation_dt'])
        print(elastic_ready_doc)
        elastic_json_record = json.dumps(elastic_ready_doc)
        print("###"*30)
        pprint.pprint(elastic_json_record)
        store_record(es_conn,'datacube',elastic_json_record)



# ################# MAIN ################### #

# get parameters here later hard code for now

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

my_bucket = 'lsaa-staging-cog'
top_directory_prefix = "L08/2014/042/034/"
elastic_all_metatdata(my_bucket, top_directory_prefix)

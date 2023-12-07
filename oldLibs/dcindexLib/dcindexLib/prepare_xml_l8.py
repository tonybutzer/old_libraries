
"""
Open Data Cube Prepare Script 

and as always seems to be a Work in Progress -- WIP!

Testing this with local USB Drive Data over Rwanda

This script crawls a rwanda director of &*.xml files

* 1. locates the xml metadata
* 2. creates a gneric metaBlob from xml (could be done for json or MTL) blob for each metadata file 
* 3. loads these into the postgresql database as a JSONB blob object - using odc dc routine:
    add_dataset(...):

"""

import logging
import datacube
from datacube.scripts.dataset import create_dataset, parse_match_rules_options
from datacube.utils import changes
from dcindexLib.generic_prepare import make_rules, satellite_ref, get_band_file_map, add_dataset
from dcindexLib.xml_meta_lib import get_metadata_docs




def add_all_datacube_datasets(top_directory_name):
    """ Main loop function to traverse the bucket-->prefix tree and index each dataset

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

    dc = datacube.Datacube()
    index = dc.index
    rules = make_rules(index, product_list = ['l8_rwanda',])
    # print(type(rules))
    # print(rules)
    for metadata_path, metadata_doc in get_metadata_docs(top_directory_name):
        uri = metadata_path
        add_dataset(metadata_doc, uri, rules, index)
        logging.info("Indexing %s", metadata_path)



# ################# MAIN ################### #

# get parameters here later hard code for now

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

top_directory_name = "/mnt/rwanda/LC08"
add_all_datacube_datasets(top_directory_name)

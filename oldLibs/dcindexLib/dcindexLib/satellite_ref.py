
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

import datacube
from datacube.scripts.dataset import create_dataset, parse_match_rules_options
from datacube.utils import changes
from dcindexLib.generic_prepare import make_rules, satellite_ref, get_band_file_map, add_dataset
import logging
import os
import uuid
import boto3


from dcindexLib.xml_meta_blob import MetaBlob
from dcindexLib.projection_stuff import get_projection_info


def file_walk(directory):
    for root, dirs, files in os.walk(directory):
        # path = root.split(os.sep)
        # print((len(path) - 1) * '---', os.path.basename(root))
        # print("ROOT:",root)
        for file in files:
            if ".xml" in file and not "aux" in file:
                # print(len(path) * '---', file)
                full_file = root + '/' + file
                yield full_file


def get_files_from_dir(directory):
    f = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        f.extend(filenames)
        break
    return (dirnames, filenames)


def get_xml_string(file):
    """ read xml into memory from xml_meta_file """

    with open(file, 'r') as content_file:
        content = content_file.read()
    # print (content)
    return content



def make_doc_from_meta_blob_SAVE(xml_string, type, directory, meta_file_name):
    """ just does xml for now - need to add MTL and json """
    logging.info("Meta Blob %s", meta_file_name)
    if xml_string is None:
        xml_raw = get_xml_string(meta_file_name)
    else:
        xml_raw = xml_string
    meta_blob = MetaBlob(directory, xml_raw)
    meta_blob.get_global_metadata()

    #### 
    level = meta_blob.product_id.split('_')[1]
    images, product_type = satellite_ref(meta_blob.satellite)
    print("IMAGES",images)
    center_dt = meta_blob.acquisition_date + " " + meta_blob.scene_center_time
    start_time = center_dt
    end_time = center_dt

    #####

    print("BAND 4 SR: ", meta_blob.band_dict['sr_band4'])

    geo_guinea_pig = meta_blob.band_dict['sr_band4']

    spatial_ref = get_projection_info(geo_guinea_pig)
    

    westxf = float(meta_blob.westx) * 1.0
    eastxf = float(meta_blob.eastx) * 1.0
    northyf = float(meta_blob.northy) * 1.0
    southyf = float(meta_blob.southy) * 1.0

    geo_ref_points = {
          'ul':
             {'x': westxf,
              'y': northyf},
          'ur':
             {'x': eastxf,
              'y': northyf},
          'lr':
             {'x': eastxf,
              'y': southyf},
          'll':
             {'x': westxf,
              'y': southyf}}

    print("COORD=", meta_blob.coord)
    print("UPPER_LEFT=", geo_ref_points['ul'])
    docdict = {
        'id': str(uuid.uuid4()),
        'processing_level': str(level),
        'product_type': product_type,
        'creation_dt': meta_blob.acquisition_date,
        'platform': {'code': meta_blob.satellite},
        'instrument': {'name': meta_blob.instrument},
        'extent': {
            'from_dt': str(start_time),
            'to_dt': str(end_time),
            'center_dt': str(center_dt),
            'coord': meta_blob.coord,
        },
        'format': {'name': 'GeoTiff'},

        'grid_spatial': {
            'projection': {
                'geo_ref_points': geo_ref_points,
                'spatial_reference': spatial_ref,
            }
        },
        'image': {
            'bands': {
                image[1]: {
                    'path': meta_blob.band_dict[get_band_file_map(image[1])],
                    'layer': 1,
                } for image in images
            }
        },

        'lineage': {'source_datasets': {}}
    }
    # print (docdict)
    return docdict

def make_doc_from_meta_blob(xml_string, type, directory, meta_file_name):
    """ just does xml for now - need to add MTL and json """
    logging.info("Meta Blob %s", meta_file_name)
    if xml_string is None:
        xml_raw = get_xml_string(meta_file_name)
    else:
        xml_raw = xml_string
    meta_blob = MetaBlob(directory, xml_raw)
    meta_blob.get_global_metadata()

    #### 
    level = meta_blob.product_id.split('_')[1]
    images, product_type = satellite_ref(meta_blob.satellite)
    print("IMAGES",images)
    center_dt = meta_blob.acquisition_date + " " + meta_blob.scene_center_time
    start_time = center_dt
    end_time = center_dt

    #####

    print("BAND 4 SR: ", meta_blob.band_dict['sr_band4'])

    geo_guinea_pig = meta_blob.band_dict['sr_band4']

    # spatial_ref = get_projection_info(geo_guinea_pig)

    # TONY FIX ythie HARDCODE soon!

    spatial_ref = 'epsg:5072'
    

    westxf = float(meta_blob.westx) * 1.0
    eastxf = float(meta_blob.eastx) * 1.0
    northyf = float(meta_blob.northy) * 1.0
    southyf = float(meta_blob.southy) * 1.0

    geo_ref_points = {
          'ul':
             {'x': westxf,
              'y': northyf},
          'ur':
             {'x': eastxf,
              'y': northyf},
          'lr':
             {'x': eastxf,
              'y': southyf},
          'll':
             {'x': westxf,
              'y': southyf}}

    print("COORD=", meta_blob.coord)
    print("UPPER_LEFT=", geo_ref_points['ul'])
    docdict = {
        'id': str(uuid.uuid4()),
        'processing_level': str(level),
        'product_type': product_type,
        'creation_dt': meta_blob.acquisition_date,
        'platform': {'code': meta_blob.satellite},
        'instrument': {'name': meta_blob.instrument},
        'extent': {
            'from_dt': str(start_time),
            'to_dt': str(end_time),
            'center_dt': str(center_dt),
            'coord': meta_blob.coord,
        },
        'format': {'name': 'GeoTiff'},

        'grid_spatial': {
            'projection': {
                'geo_ref_points': geo_ref_points,
                'spatial_reference': spatial_ref,
            }
        },
        'image': {
            'bands': {
                image[1]: {
                    'path': meta_blob.band_dict[get_band_file_map(image[1])],
                    'layer': 1,
                } for image in images
            }
        },

        'lineage': {'source_datasets': {}}
    }
    # print (docdict)
    return docdict


def get_metadata_docs(directory):
    """ GENERATOR: recursively find the metadata for each scene/tile

    Args:
        Top Directory

    """
    for file in file_walk(directory):

            # metadata_doc = make_doc_from_json(raw_string, bucket_name, obj_key)
        meta_file_name = file
        # metadata_doc = {}
        meta_type = 'xml'
        dir_name = os.path.dirname(meta_file_name)
        metadata_doc = make_doc_from_meta_blob(meta_type, dir_name, meta_file_name)

        yield meta_file_name, metadata_doc

def get_metadata_docs_bucket(bucket_name, prefix):
    """ GENERATOR: recursively find the metadata for each scene/tile

    Args:
        Top bucket path

    """

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    logging.info("Bucket : %s", bucket_name)
    for obj in bucket.objects.filter(Prefix=prefix):
        if obj.key.endswith('.xml') and not "aux" in obj.key:
            obj_key = obj.key
            logging.info("Processing %s", obj_key)
            raw_string = obj.get()['Body'].read().decode('utf8')
            # print(raw_string)
            meta_type = 'xml'
            dir_name=prefix
            meta_file_name=obj_key
            print("DIRNAME:", dir_name, "META:", meta_file_name)
            my_dir = dir_name = os.path.dirname(meta_file_name)
            print("MYDIR:", my_dir, "META:", meta_file_name)
            my_dir = "s3://" + bucket_name + '/'  + my_dir

            metadata_doc = make_doc_from_meta_blob(raw_string, meta_type, my_dir, meta_file_name)
            #metadata_doc = make_xml_doc(raw_string,bucket_name, obj_key)
            # print(metadata_doc)
            # TONY
            yield obj_key, metadata_doc


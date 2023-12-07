
import boto3
import logging
import uuid
from .meta_blob_from_json import MetaBlob

from dcindexLib.generic_prepare import make_rules, satellite_ref, get_band_file_map, add_dataset

def make_doc_from_json(raw_json, bucket_name, object_key):
    """ creates a json blob called a doc for insetion into the database index

    Args:
        **raw_json**

        **bucket_name**

        **object_key** (str): AWS S3 key to the json file name

    """

    # print(object_key)

    s3prefix = '/'.join(object_key.split("/")[:-1])
    s3path = 's3://{bucket_name}/{s3prefix}'.format(
        bucket_name=bucket_name, s3prefix=s3prefix)

    # print(s3path)

    meta_blob = MetaBlob(raw_json)

    level = meta_blob.product_id.split('_')[1]
    images, product_type = satellite_ref(meta_blob.satellite)
    center_dt = meta_blob.acquisition_date + " " + meta_blob.scene_center_time
    start_time = center_dt
    end_time = center_dt

    # HARDCODE - please fix this Tony
    cs_code = '5072'
    spatial_ref = 'epsg:' + cs_code

    
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

    print("TONY GEO:", geo_ref_points)
        
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
                    'path': s3path + '/' + meta_blob.file_dict[get_band_file_map(image[1])],
                    'layer': 1,
                } for image in images
            }
        },

        'lineage': {'source_datasets': {}}
    }
    # print (docdict)
    # print("TONY make xml")
    # docdict = absolutify_paths(docdict, bucket_name, object_key)
    # print (docdict)
    # print("TONY")
    return docdict


def get_metadata_docs_json(bucket_name, prefix):
    """ GENERATOR: recursively find the metadata for each scene/tile

    Args:
        **bucket_name** (str): AWS S3 Bucket Name - example lsaa-staging-cog

        **prefix** (str): AWS prefix within the bucket to start the recursive search for .json file = example L8
    """

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    logging.info("Bucket : %s", bucket_name)
    print(bucket_name, prefix)
    for obj in bucket.objects.filter(Prefix=prefix):
        # print(obj.key)
        if obj.key.endswith('.json') and not "ANG" in obj.key and not "MTL" in obj.key:
            obj_key = obj.key
            logging.info("Processing %s", obj_key)
            raw_string = obj.get()['Body'].read().decode('utf8')
            metadata_doc = make_doc_from_json(raw_string, bucket_name, obj_key)

            yield obj_key, metadata_doc



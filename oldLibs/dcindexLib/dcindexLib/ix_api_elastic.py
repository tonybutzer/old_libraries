import logging
import json
import pprint

from dcindexLib.elastic_index import connect_elasticsearch
from dcindexLib.elastic_index import l_create_index
from dcindexLib.elastic_index import store_record
from dcindexLib.elastic_meta import get_metadata_docs_json, elastic_flatten_doc
from dcindexLib.parse_MTL import get_metadata_docs_MTL


def ix_elastic_all_metatdata_json(index_name, record_type, bucket, top_directory_prefix):
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
    es_conn.indices.delete(index='cube', ignore=[400, 404])

    # create new elastic search index
    l_create_index(es_conn, index_name, record_type)

    #for metadata_path, metadata_doc in get_metadata_docs_bucket(bucket, top_directory_prefix):
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
        store_record(es_conn, index_name, record_type, elastic_json_record)



def ix_elastic_all_metatdata_MTL(index_name, record_type, bucket, top_directory_prefix):
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
    es_conn.indices.delete(index='cube', ignore=[400, 404])

    # create new elastic search index
    l_create_index(es_conn, index_name, record_type)

    for metadata_path, metadata_doc in get_metadata_docs_MTL(bucket, top_directory_prefix):
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
        store_record(es_conn, index_name, record_type, elastic_json_record)




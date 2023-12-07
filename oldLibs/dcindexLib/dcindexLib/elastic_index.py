from elasticsearch import Elasticsearch


def connect_elasticsearch():
    _es = None
    #_es = Elasticsearch([{'host': 'elastic', 'port': 9200}])
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es


def store_record(elastic_object, index_name, record_type, record):
    try:
        outcome = elastic_object.index(index=index_name, doc_type=record_type, body=record)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))



def l_create_index(es_object, index_name, record_type):
    """ Example create_index needs to be tuned for datacube metadata """

    created = False
    bands = ['red', 'green', 'blue', 'nir', 'pixel_qa']

    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            record_type: {
                "dynamic": "strict",
                "properties": {
                    "footprint" : {
                            "type": "geo_shape"
                    },
                    "ul" : {
                            "type": "geo_point"
                    },
                    "processing_level": {
                        "type": "text"
                    },
                    "creation_dt": {
                        "type": "date",
                        "format": "yyyy-MM-dd||yyyy"
                    },
                }
            }
        }
    }

    for band in bands:
        settings['mappings'][record_type]['properties'][band] = {'type': 'text'}
    
    # pprint.pprint (settings)

    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created

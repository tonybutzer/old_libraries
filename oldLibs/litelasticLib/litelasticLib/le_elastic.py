""" elastic search interface routines """


import json
import pprint
from datetime import datetime
from elasticsearch import Elasticsearch
import pygeoj

## from .lc_geometry import return_aoi_polygon


def lc_connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'elastic', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es


def return_elastic_hits(es_index, es_type, aoi_geojson_file, time):

    mybody = return_geo_query_body(aoi_geojson_file, time = time)

    elastic_json_record = json.dumps(mybody)
    # print("MYBODY:", type(elastic_json_record))
    # print(elastic_json_record)
    # pprint.pprint(elastic_json_record)
    
    client = lc_connect_elasticsearch()

    response = client.search( index=es_index,size=1400, body=elastic_json_record)

    HIT_LIST = response['hits']['hits']
    return HIT_LIST


def _return_date_query(time):

    t0 = str(datetime.date(time[0]))
    t1 = str(datetime.date(time[1]))

    date_query = [{"range": {"creation_dt": {"gte": t0}}},
              {"range": {"creation_dt": {"lt": t1}}}]
    return date_query


def _return_geo_walk_poly(geo_file):
    testfile = pygeoj.load(geo_file)
    for feature in testfile:
        #print (feature.geometry.type)
        #print (feature.geometry.coordinates)
        foot = {
            "type": feature.geometry.type,
            "coordinates": feature.geometry.coordinates
        }
        return (foot)

def return_geo_query_body(geo_file, time):

    #geo_poly = return_aoi_polygon(ul, lr)
    geo_poly = _return_geo_walk_poly(geo_file)

    range_list = _return_date_query(time)

    geo_filter_body = {"query": {
    "bool": {
      "must": range_list,
      "filter": [ {
      "geo_shape": {
                    "footprint": {
                        "shape": { 
                        "type": geo_poly['type'],
                        "coordinates": geo_poly['coordinates']
                        },
                        #"relation": "within"
                        "relation": "contains"
                    }
                }
      }
      ]
    }
    }}

    return geo_filter_body

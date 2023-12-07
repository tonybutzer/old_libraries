import yaml
import json
import pandas as pd
from pystac_client import Client

def get_stac_catalog_dict():
    with open('stac_catalogs.yaml') as fl:
        conf = yaml.safe_load(fl)
    return conf

def _make_df_dict(item):
    the_d = {}
    the_d['product'] = 'usgs-landsat-ard-collection02-sr'
    the_d['date'] = item['properties']['datetime']
    the_d['grid'] = item['properties']['landsat:grid_region']
    the_d['h'] = item['properties']['landsat:grid_horizontal']
    the_d['v'] = item['properties']['landsat:grid_vertical']
    #'eo:cloud_cover', 'landsat:cloud_shadow_cover', 'landsat:snow_ice_cover', 'landsat:fill'
    the_d['cc'] = item['properties']['eo:cloud_cover']
    the_d['fill'] = item['properties']['landsat:fill']

    try:
        for ky in item['assets'].keys():
            #print(ky)
            if 'index' not in ky and 'coastal' not in ky and 'qa_' not in ky:
                the_d[ky] = item['assets'][ky]['alternate']['s3']['href']
    except Exception as error:
        print("BAD DATE: ", the_d['date'])
        print("the error is: ", error)
    return the_d

def _create_df(items_dict):
    panda_list=[]
    for it in items_dict:
        d = _make_df_dict(it)
        panda_list.append(d)
    DF = pd.DataFrame(panda_list)
    return DF

class Astac: # ard stac class
    def __init__(self, stac_config, collection_of_interest=None):
        self.stac_config = stac_config
        if collection_of_interest is not None:
            self.stac_collection = collection_of_interest
        else:
            self.stac_collection = self.stac_config['fav_collection']
        print(stac_config['url'])
        self.client = Client.open(stac_config['url'])


    def collection(self):
        return self.stac_collection

    def description(self):
        return self.stac_config['description']

    def get_my_assets(self, aoi_geojson, h, v, date_range_text, cloud_cover_pct_max):
        print(aoi_geojson, date_range_text, cloud_cover_pct_max)

        if h is None or v is None:
            search_ard = self.client.search(collections=[self.stac_collection],
                                intersects=json.load(open(aoi_geojson, 'r'))['features'][0]['geometry'],
                                datetime = date_range_text,
                                query = [f"eo:cloud_cover<{cloud_cover_pct_max}"],
                                limit = 100)
            stuff_ard = search_ard.get_all_items_as_dict()['features']
            print(f"{search_ard.matched()} items found")
        else:
            if aoi_geojson is None:
                intersects = None
            else:
                intersects = json.load(open(aoi_geojson, 'r'))['features'][0]['geometry']
                
            search_ard = self.client.search(
                collections = [self.stac_collection],
                datetime = date_range_text,
                query = [f"eo:cloud_cover<{cloud_cover_pct_max}", f'landsat:grid_horizontal={h}', f'landsat:grid_vertical={v}', 'landsat:grid_region=CU'],
                limit = 100)
            stuff_ard = search_ard.get_all_items_as_dict()['features']
            print(f"{search_ard.matched()} items found")
    
        return(stuff_ard)

    def fav_fields_df(self, item_dict_list):
        DF = _create_df(item_dict_list)
        return DF

# aoi = gpd.read_file('AOI/maine1.geojson')
# geom = json.loads(aoi['geometry'].to_json())['features'][0]['geometry']

# # limit sets the # of items per page so we can see multiple pages getting fetched
# search = cat.search(
#     collections = [collection_id],
#     intersects = aoi['geometry'][0],
#     datetime = "2021-01-01/2021-03-31",
#     query = ["eo:cloud_cover<10"],
#     limit = 100
# )




    def collections_list(self):
        collection_list = []
        for collection_child in self.client.get_children():
            collection_list.append(collection_child.id)
        return(collection_list)

    def collections_df(self):
        collections = [(c.id, c.title) for c in self.client.get_collections()]
        pd.set_option("display.max_colwidth", 150)
        df = pd.DataFrame(collections, columns=['id', 'title'])
        return df
        

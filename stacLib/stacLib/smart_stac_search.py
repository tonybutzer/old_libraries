#import yaml
import json
import pandas as pd
from pystac_client import Client

def _make_df_dict(item):
    the_d = {}
    the_d['product'] = 'sentinel-2-cog'
    the_d['date'] = item['properties']['datetime']
    #'eo:cloud_cover', 'landsat:cloud_shadow_cover', 'landsat:snow_ice_cover', 'landsat:fill'
    the_d['cc'] = item['properties']['eo:cloud_cover']

    try:
        for ky in item['assets'].keys():
            #print(ky)
            if 'index' not in ky and 'coastal' not in ky and 'qa_' not in ky:
                the_d[ky] = item['assets'][ky]['href']
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

def _get_smart_key():
    # Using readlines()
    file1 = open('/home/ec2-user/.apikey', 'r')
    Lines = file1.readlines()
    for l in Lines:
        if l.startswith('smart_api_key'):
            my_key = l.split('=')[-1].strip()
            return my_key

class Smartstac: # ard stac class

    def __init__(self, collection):
        self.catalog_url = 'https://api.smart-stac.com'
        self.fav_collection = collection
        self.stac_collection = self.fav_collection
        apikey = _get_smart_key()
        self.client = Client.open(self.catalog_url, headers={'x-api-key': apikey})
        print(self.catalog_url, self.fav_collection)


    def collection(self):
        return self.stac_collection

    def description(self):
        return self.stac_config['description']

    def get_my_assets(self, aoi_geojson, date_range_text, cloud_cover_pct_max):
        print(aoi_geojson, date_range_text, cloud_cover_pct_max)

        my_intersects = json.load(open(aoi_geojson, 'r'))['features'][0]['geometry']
                
        search_s2 = self.client.search(
                collections = [self.stac_collection],
                datetime = date_range_text,
                intersects = my_intersects,
                query = [f"eo:cloud_cover<{cloud_cover_pct_max}", ],
                limit = 100)
        stuff_s2 = search_s2.get_all_items_as_dict()['features']
        print(f"{search_s2.matched()} items found")
    
        return(stuff_s2)

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
        

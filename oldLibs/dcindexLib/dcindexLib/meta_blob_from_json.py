"""

This module contains the MetaBlob class for holding a dictionary (dict) of satellite metadata
read from a .json file created by someone in LSAA - for the DevSeed Prototype Raft application

more to come ...

watch this space ...

"""

import json
from pyproj import Proj

class MetaBlob:

    def __init__(self, raw_json):
        # print(raw_json)
        self.json_data = json.loads(raw_json)
        # self.dump()
        self.set_global_metadata()
        self.set_geography_coords()
        #self.get_geography_coords()
        self.set_projection_coords()
        #self.get_projection_coords()
        self.set_band_file_names()


    def dump(self):
        json_data = self.json_data
        print(json_data)
        print("===" *60)
        print("===" *60)
        print(json_data['espa_metadata']['global_metadata'])


    def set_global_metadata(self):
        json_data = self.json_data
        self.data_provider = json_data['espa_metadata']['global_metadata']['data_provider']
        self.satellite = json_data['espa_metadata']['global_metadata']['satellite']
        self.instrument = json_data['espa_metadata']['global_metadata']['instrument']
        self.acquisition_date = json_data['espa_metadata']['global_metadata']['acquisition_date']
        self.scene_center_time = json_data['espa_metadata']['global_metadata']['scene_center_time']
        self.product_id = json_data['espa_metadata']['global_metadata']['product_id']
        self.lpgs_metadata_file = json_data['espa_metadata']['global_metadata']['lpgs_metadata_file']



    def get_global_metadata(self):
        print (self.data_provider)
        print (self.satellite)
        print (self.instrument)
        print (self.acquisition_date)
        print (self.scene_center_time)
        print (self.product_id)
        print (self.lpgs_metadata_file)


    def set_geography_coords(self):
        json_data = self.json_data
        self.west = json_data['espa_metadata']['global_metadata']['bounding_coordinates']['west']
        self.east = json_data['espa_metadata']['global_metadata']['bounding_coordinates']['east']
        self.north = json_data['espa_metadata']['global_metadata']['bounding_coordinates']['north']
        self.south = json_data['espa_metadata']['global_metadata']['bounding_coordinates']['south']

        # self.coord = {
          # 'ul':
             # {'lon': self.west,
              # 'lat': self.north},
          # 'ur':
             # {'lon': self.east,
              # 'lat': self.north},
          # 'lr':
             # {'lon': self.east,
              # 'lat': self.south},
          # 'll':
             # {'lon': self.west,
              # 'lat': self.south}}



    def get_geography_coords(self):
        print(self.west)
        print(self.east)
        print(self.north)
        print(self.south)
        print(self.coord)


    def set_projection_coords(self):
        json_data = self.json_data
        self.projection_information = json_data['espa_metadata']['global_metadata']['projection_information']
        corner_points = json_data['espa_metadata']['global_metadata']['projection_information']['corner_point']
        for cp in corner_points:
            if cp['@location'] in 'UL':
                self.westx = cp['@x']
                self.northy = cp['@y']
                print("WN:", self.westx, self.northy)
            if cp['@location'] in 'LR':
                self.eastx = cp['@x']
                self.southy = cp['@y']
                print("ES:", self.eastx, self.southy)

        geo_ulxy = _geo_untranslate(self.westx, self.northy)
        geo_urxy = _geo_untranslate(self.eastx, self.northy)
        geo_lrxy = _geo_untranslate(self.eastx, self.southy)
        geo_llxy = _geo_untranslate(self.westx, self.southy)
        self.coord = {
          'ul':
             {'lon': geo_ulxy[1],
              'lat': geo_ulxy[0]},
          'ur':
             {'lon': geo_urxy[1],
              'lat': geo_urxy[0]},
          'lr':
             {'lon': geo_lrxy[1],
              'lat': geo_lrxy[0]},
          'll':
             {'lon': geo_llxy[1],
              'lat': geo_llxy[0]}}



    def get_projection_coords(self):
        #print(self.projection_information)
        print(self.westx)
        print(self.eastx)
        print(self.northy)
        print(self.southy)


    def set_band_file_names(self):
        band_array = self.json_data['espa_metadata']['bands']['band']
        print("LEN", len(band_array))
        self.file_dict = {}
        for band in band_array:
            # print(band['@name'])
            # print(band['file_name'])
            name = band['@name']
            file_name = band['file_name']
            file_name = file_name.replace("tif", "TIF")
            self.file_dict[name] = file_name

        print(self.file_dict)


def _geo_translate(lat,lon,epsg="epsg:5072"):
    """ converts lat lon to albers X and Y

        Returns: x, y
    """
    # print(lat,lon)

    p = Proj(init=epsg) # EPSG code AEA


    x,y = p(lon,lat)

    # print(x,y)
    return(x,y)


def _geo_untranslate(x,y,epsg="epsg:5072"):
    """ converts albers X and Y to lat, lon

        Returns: lat, lon
    """
    # print(x,y)

    p = Proj(init=epsg) # EPSG code AEA


    glon, glat = p(x, y, inverse=True)


    # print(glat,glon)
    return(glat,glon)


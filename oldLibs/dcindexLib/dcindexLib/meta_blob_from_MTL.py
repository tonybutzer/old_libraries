from osgeo import osr

from dcindexLib.generic_prepare import satellite_ref
"""

MTL metadata parsing

This module contains the MetaBlob class for holding a dictionary (dict) of satellite metadata
read from a .MTL file created by someone in espaLand

more to come ...

watch this space ...

"""

def get_geo_ref_points(info):
    return {
        'ul': {'x': info['CORNER_UL_PROJECTION_X_PRODUCT'], 'y': info['CORNER_UL_PROJECTION_Y_PRODUCT']},
        'ur': {'x': info['CORNER_UR_PROJECTION_X_PRODUCT'], 'y': info['CORNER_UR_PROJECTION_Y_PRODUCT']},
        'll': {'x': info['CORNER_LL_PROJECTION_X_PRODUCT'], 'y': info['CORNER_LL_PROJECTION_Y_PRODUCT']},
        'lr': {'x': info['CORNER_LR_PROJECTION_X_PRODUCT'], 'y': info['CORNER_LR_PROJECTION_Y_PRODUCT']},
    }


def get_coords(geo_ref_points, spatial_ref):
    t = osr.CoordinateTransformation(spatial_ref, spatial_ref.CloneGeogCS())

    def transform(p):
        lon, lat, z = t.TransformPoint(p['x'], p['y'])
        return {'lon': lon, 'lat': lat}

    return {key: transform(p) for key, p in geo_ref_points.items()}

# import re
import pprint
# from xml.etree import ElementTree

class MetaBlob:


    def __init__(self, directory, raw_MTL):

        self.directory = directory
        self.mtlstring = raw_MTL
        self.set_global_metadata()
        self.set_geography_coords()
        # self.set_projection_coords()
        self.set_band_file_names()


    def set_global_metadata(self):
        mtl_data = self.mtlstring

        self.data_provider = 'UKNOWN'
        mtl_product_info = mtl_data['PRODUCT_METADATA']
        mtl_metadata_info = mtl_data['METADATA_FILE_INFO']
        satellite = mtl_product_info['SPACECRAFT_ID']
        self.satellite = satellite
        self.instrument = mtl_product_info['SENSOR_ID']
        self.acquisition_date = mtl_product_info['DATE_ACQUIRED']
        self.scene_center_time = mtl_product_info['SCENE_CENTER_TIME']
        self.product_id = mtl_product_info['DATA_TYPE']
        self.lpgs_metadata_file = "A.MTL"


    def get_global_metadata(self):
        print (self.data_provider)
        print (self.satellite)
        print (self.instrument)
        print (self.acquisition_date)
        print (self.scene_center_time)
        print (self.product_id)
        print (self.lpgs_metadata_file)



    def set_geography_coords(self):
        mtl_data = self.mtlstring
        cs_code = 32600 + mtl_data['PROJECTION_PARAMETERS']['UTM_ZONE']
        spatial_ref = osr.SpatialReference()
        spatial_ref.ImportFromEPSG(cs_code)
        self.spatial_ref = spatial_ref
        self.cs_code = cs_code
        mtl_product_info = mtl_data['PRODUCT_METADATA']
        geo_ref_points = get_geo_ref_points(mtl_product_info)
        self.geo_ref_points = geo_ref_points
        coordinates = get_coords(geo_ref_points, spatial_ref)
        self.coord = coordinates


    def get_geography_coords(self):
        print(self.west)
        print(self.east)
        print(self.north)
        print(self.south)
        print(self.coord)

    def set_projection_coords(self):
        xmlstring = self.xmlstring

        xmlstring = re.sub(r'\sxmlns="[^"]+"', '', xmlstring, count=1)
        doc = ElementTree.fromstring(xmlstring)
        projection_parameters = doc.find('.//projection_information')
        for corner_point in projection_parameters.findall('corner_point'):
            if corner_point.attrib['location'] in 'UL':
                self.westx = corner_point.attrib['x']
                self.northy = corner_point.attrib['y']
            if corner_point.attrib['location'] in 'LR':
                self.eastx = corner_point.attrib['x']
                self.southy = corner_point.attrib['y']


    def get_projection_coords(self):
        #print(self.projection_information)
        print(self.westx)
        print(self.eastx)
        print(self.northy)
        print(self.southy)


    def set_band_file_names(self):
        self.file_dict = {}
        mtl_data = self.mtlstring
        mtl_product_info = mtl_data['PRODUCT_METADATA']
        satellite = mtl_product_info['SPACECRAFT_ID']
        bands, prod_type  = satellite_ref(satellite)

        for band in bands:
            print(band)
            print(band[0][0])
            #print(band[0][1])
            band_num, band_name = band
            # band_file_name = mtl_product_info['FILE_NAME_BAND_' + band[0][0]]
            band_file_name = mtl_product_info['FILE_NAME_BAND_' + band_num]
            print(band_name)
            self.file_dict[band_name] = band_file_name
        pp = pprint.PrettyPrinter(depth=6)
        pp.pprint (self.file_dict)


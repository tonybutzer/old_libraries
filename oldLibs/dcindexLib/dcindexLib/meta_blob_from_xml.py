"""

XML metadata parsing

This module contains the MetaBlob class for holding a dictionary (dict) of satellite metadata
read from a .xml file created by someone in espaLand

more to come ...

watch this space ...

"""

import re
import pprint
from xml.etree import ElementTree

class MetaBlob:


    def __init__(self, directory, raw_xml):

        self.directory = directory
        self.xmlstring = raw_xml 
        self.set_global_metadata()
        self.set_geography_coords()
        self.set_projection_coords()
        self.set_band_file_names()

    def set_global_metadata(self):
        xmlstring = self.xmlstring

        xmlstring = re.sub(r'\sxmlns="[^"]+"', '', xmlstring, count=1)
        doc = ElementTree.fromstring(xmlstring)
        
        self.data_provider = doc.find('.//data_provider').text
        self.satellite = doc.find('.//satellite').text
        self.instrument = doc.find('.//instrument').text
        self.acquisition_date = doc.find('.//acquisition_date').text
        self.scene_center_time = doc.find('.//scene_center_time').text
        self.product_id =  doc.find('.//product_id').text
        self.lpgs_metadata_file = doc.find('.//lpgs_metadata_file').text



    def get_global_metadata(self):
        print (self.data_provider)
        print (self.satellite)
        print (self.instrument)
        print (self.acquisition_date)
        print (self.scene_center_time)
        print (self.product_id)
        print (self.lpgs_metadata_file)



    def set_geography_coords(self):
        xmlstring = self.xmlstring

        xmlstring = re.sub(r'\sxmlns="[^"]+"', '', xmlstring, count=1)
        doc = ElementTree.fromstring(xmlstring)

        self.west = doc.find('.//bounding_coordinates/west').text
        self.east = doc.find('.//bounding_coordinates/east').text
        self.north = doc.find('.//bounding_coordinates/north').text
        self.south = doc.find('.//bounding_coordinates/south').text

        self.coord = {
          'ul':
             {'lon': self.west,
              'lat': self.north},
          'ur':
             {'lon': self.east,
              'lat': self.north},
          'lr':
             {'lon': self.east,
              'lat': self.south},
          'll':
             {'lon': self.west,
              'lat': self.south}}


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
        """ parse the xml metadata and return the band names in a dict """
        self.band_dict = {}
        xmlstring = self.xmlstring
        xmlstring = re.sub(r'\sxmlns="[^"]+"', '', xmlstring, count=1)
        doc = ElementTree.fromstring(xmlstring)
        # print(type(xmldoc))
        bands = doc.find('.//bands')
        for bandxml in bands:
            band_name = (bandxml.get('name'))
            #print(band_name)
            file = bandxml.find('.//file_name')
            band_file_name = self.directory + '/' +file.text
            # print(band_file_name)
            self.band_dict[band_name] = band_file_name
        pp = pprint.PrettyPrinter(depth=6)
        pp.pprint (self.band_dict)


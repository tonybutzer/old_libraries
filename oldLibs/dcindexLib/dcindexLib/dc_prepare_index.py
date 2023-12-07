""" this code indexes xml data into the OpenDataCube postgres database for use by dc.load() etc. """

import os


from dcindexLib.xml_meta_blob import MetaBlob

def get_xml_string(file):

    with open(file, 'r') as content_file:
        content = content_file.read()
    print (content)
    return content



if __name__ == "__main__":
    file = "/mnt/rwanda/LE07/173/061/2015/LE071730612015082801T1-SC20181201020124/LE07_L1TP_173061_20150828_20161021_01_T1.xml"
    xml_raw = get_xml_string(file)
    directory = os.path.dirname(file)
    print(directory)
    mb = MetaBlob(directory, xml_raw)
    mb.get_global_metadata()
    mb.get_geography_coords()
    mb.get_projection_coords()

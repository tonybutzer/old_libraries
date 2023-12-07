""" this is where the external interfaces will go """

"""
[Python Tutorial: Datetime Module - How to work with Dates, Times, Timedeltas, and Timezones](https://www.youtube.com/watch?v=eirjjyP2qcQ)

"""

from collections import OrderedDict
from datetime import datetime
import pandas as pd
from .le_elastic import return_elastic_hits
from xarrayLib.xr_xarray import build_the_xarray


class Lecube():

    def __init__(self):
        print("creating Lilcube class")


    def search(self, es_index, es_type, aoi_geojson_file_name, time, measurements):
        print("Your Index is:", es_index)
        print("Your Record Type for this index is:", es_type)
        # print(time)
        d = datetime.date(time[0])
        # print(d)
        hit_list = return_elastic_hits(es_index, es_type, aoi_geojson_file_name, time)
        # print("HIT COUNT =", len(hit_list))
        DF = make_hits_dataframe(hit_list)
        return DF


    def load(self, aoi_geojson_file_name, measurements, panda_df):
        # bbox = bounding_box_tuple_from_geojson(aoi_geojson_file_name)
        # aoi = AOI_bounding_box((30.209661,-2.218817,30.246396,-2.163926))
        # aoi = AOI_bounding_box((bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1]))

        THE_XARRAY = build_the_xarray(aoi_geojson_file_name, measurements, panda_df)
        return (THE_XARRAY)
        # return(bbox)


def make_hits_dataframe(hit_list):
    pids, bands, paths, rows, dates, reds = [], [], [], [], [], []
    greens, blues = [], []
    nirs, pixel_qas = [], []
    # print("###" *30)
    for hit in hit_list:
        src = hit['_source']

        product_id = src['red'].split('/')[-1]
        product_id = product_id.split('.tif')[0]

        path =  product_id.split('_')[2][0:3]
        row =  product_id.split('_')[2][-2:]
        date = src['creation_dt']

        product = product_id[0:9]
        band = product_id.split('_')[-1]
        red = src['red']

        green = src['green']
        blue = src['blue']
        nir = src['nir']
        pixel_qa = src['pixel_qa']

        # print(product,band,path,row,date,red,green,blue)

        pids.append(product)
        bands.append(band)
        paths.append(path)
        rows.append(row)
        dates.append(date)
        reds.append(red)
        greens.append(green)
        blues.append(blue)
        nirs.append(nir)
        pixel_qas.append(pixel_qa)


    #panda_input_dict = OrderedDict(product=pids, band=bands, path=paths, row=rows, date=dates, red=reds)
    panda_input_dict = dict(product=pids, band=bands, path=paths, row=rows, date=dates, red=reds, green=greens, blue=blues, nir=nirs, pixel_qa=pixel_qas)

    DF = pd.DataFrame(panda_input_dict, columns=['product', 'band', 'path', 'row', 'date', 'red', 'green', 'blue', 'nir', 'pixel_qa'])

    cols = DF.columns.tolist()
    # print(cols)

    return DF

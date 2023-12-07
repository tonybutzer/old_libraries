""" this is where the external interfaces will go """

"""
[Python Tutorial: Datetime Module - How to work with Dates, Times, Timedeltas, and Timezones](https://www.youtube.com/watch?v=eirjjyP2qcQ)

"""

from .ls_stac import ls_make_hits_dataframe
from xarrayLib.xr_xarray import build_the_xarray


class Litestac():

    def __init__(self):
        print("creating Litestac class")


    def search(self, aoi_geojson_file_name, time, measurements):

        DF = hit_panda_dataframe = ls_make_hits_dataframe(aoi_geojson_file_name, time)
        #hit_list = return_stac_hits(aoi_geojson_file_name, time)
        # print("HIT COUNT =", len(hit_list))
        #DF = make_hits_dataframe(hit_list)
        return DF


    def load(self, aoi_geojson_file_name, measurements, panda_df):

        THE_XARRAY = build_the_xarray(aoi_geojson_file_name, measurements, panda_df)
        return (THE_XARRAY)



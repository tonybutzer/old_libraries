""" this module calls STAC searches and returns the results """

import re
import json
import pandas as pd
from datetime import datetime
from satsearch import Search


def DEFUNCT_return_stac_hits(aoi_geojson_file, time):
    print("return_stac_hits")
    mybody = return_geo_query_body(aoi_geojson_file, time = time)



def return_geo_query_body(geo_file, time):

    with open(geo_file) as f:
        data = json.load(f)

    for feature in data['features']:
        GEOM = feature['geometry']

    print(GEOM)

    return GEOM


    

def _return_date_query(time):

    t0 = str(datetime.date(time[0]))
    t1 = str(datetime.date(time[1]))

    date_query = t0 + '/' + t1
    return date_query



def ls_make_hits_dataframe(aoi_geojson_file, time):

    pids, bands, paths, rows, dates, reds = [], [], [], [], [], []
    greens, blues = [], []
    nirs, pixel_qas = [], []


    print("return_stac_hits")
    geom = return_geo_query_body(aoi_geojson_file, time = time)

    date_range = _return_date_query(time)

    search = Search.search(intersects=geom,
            datetime=date_range,
            collection='landsat-8-l1')
    print('intersects search: %s items' % search.found())
    items = search.items()
    print('%s items' % len(items))
    print('%s collections' % len(items._collections))
    print(items._collections)


    for item in items:
        #print(item)

        product_id = item.id

        path = product_id[3:6]
        row = product_id[6:9]


        #print ("PATH ROW", path, row)
        bandd = _return_band_dict(item)
        #print(bandd['red'])

        file_part = bandd['red'].split('/')[-1]
        print(file_part)
        product = file_part[0:9]
        band = file_part.split('_')[-1]

        date = str(item.date)

        red = bandd['red']

        green = bandd['green']
        blue = bandd['blue']
        nir = bandd['nir']
        pixel_qa = bandd['BQA']


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



    panda_input_dict = dict(product=pids, band=bands, path=paths, row=rows, date=dates, red=reds, green=greens, blue=blues, nir=nirs, pixel_qa=pixel_qas)

    DF = pd.DataFrame(panda_input_dict, columns=['product', 'band', 'path', 'row', 'date', 'red', 'green', 'blue', 'nir', 'pixel_qa'])

    cols = DF.columns.tolist()

    return DF






def _return_band_dict(item):

    band_dict = {}
    for asset in item.assets:
        title = item.assets[asset]['title']
        href = item.assets[asset]['href']

        # print(asset, item.assets[asset]['href'])

        common_name = _return_common_name(asset, title)
        # print("COMMON", common_name)
        band_dict[common_name] = href
    return (band_dict)


def _return_common_name(simple_name, title):

    if "(" in title:
        m = re.search(r"\(.*\)", title)
        COMMON_NAME = m.group(0)
        COMMON_NAME = COMMON_NAME.replace('(',"")
        COMMON_NAME = COMMON_NAME.replace(')',"")
    else:
        COMMON_NAME = simple_name

    return COMMON_NAME

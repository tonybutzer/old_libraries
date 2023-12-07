""" xpart is xarray parts list for creating a common xarray from:

    - an AOI - area of interest
    - an elasticsearch index 

"""

import rasterio
import numpy
import xarray

# from .geometry import polygon, CRS, GeoBox
from .xr_geometry import geo_translate, geo_untranslate, bounding_box_tuple_from_geojson

        

class Xpart():
    '''
        this class Xpart is a convienience class to keep all the component parts
        necessary to build an xarray
        1. the shape of the rectangle for creating/sizing the numpy multidimenional array
        2. the rows and cols for subsetting the lazy load xarray to the AOI
    '''

    def __init__(self, geojson_file, redfile):
        print("thanks for constructing an  Xpart")
        print("redfile is", redfile)
        print("geojson_file is", geojson_file)
        with rasterio.open(redfile) as src:
            print(src.profile)
        crs = _sanity_check_crs(src)
        print("CRS", crs)
        self.crs = crs
        self.affine = src.transform
        bbox = bounding_box_tuple_from_geojson(geojson_file)
        self.bbox = bbox

        width, height, cols, rows = _get_xpart_properties(src, self.bbox)

        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols

        # y, x = a.shape - TBD

        self.shape = (height, width)
        self.numpy_shape = (width, height)

        print(self.width, self.height)

        # these are so wrong
        xs = numpy.arange(self.width) * self.affine.a + (self.affine.c + self.affine.a / 2)
        ys = numpy.arange(self.height) * self.affine.e + (self.affine.f + self.affine.e / 2)

        print("XS len", len(xs))
        print("YS len", len(ys))

        for x in range(0,9):
            print(xs[x],ys[x])

        self.xs = xs
        self.ys = ys


def _sanity_check_crs(src):

    tmp = str(src.crs)
    tmp = tmp.lower()
    if 'epsg' in tmp:
        return(src.crs)
    tmp = str(src.crs)
    tmp = tmp[0:3]
    tmp = tmp.lower()
    if 'epsg' in tmp:
        return(src.crs)
    else:
        # HACK this should call a more sophisticated routine
        return('EPSG:5072')


def _get_xpart_properties(src, bbox):
    # print("TONY1", bbox)
    # print("TONY1", src.crs)
    crs = _sanity_check_crs(src)
    x1,y1 = geo_translate(bbox[0][1], bbox[0][0], crs)
    x2,y2 = geo_translate(bbox[1][1], bbox[1][0], crs)

    # print("TONY1",x1,y1)
    # print("TONY1",x2,y2)

    row1,col1 = src.index(x1,y1)
    row2,col2 = src.index(x2,y2)

    colwidth = col2 - col1
    rowheight = row2 - row1

    # print("TONY0 colwidth, rowheight",colwidth, rowheight)
    # # print("TONY0 cols",col1, col2)
    # print("TONY0 rows",row1, row2)
    return(colwidth, rowheight, (col1, col2), (row1, row2))
    #return(300, 512, (2900, 3200), (6200, 6712))

def _get_actual_rows_cols(geoTiff, bbox):
    with rasterio.open(geoTiff)as src:
        colwidth, rowheight, cols, rows = _get_xpart_properties(src, bbox)
        return(rows, cols)





def read_data_from_geotiff(databuf, index, color, xpart, df):
    '''
        color is really short for band .i.e red, nir etc.
    '''
    geoTiff = df.iloc[index][color]
    # Note that the blocksize of the image is 256 by 256, so we want xarray to use some multiple of that
    xchunk = 2048
    ychunk = 2048
    #da = xarray.open_rasterio(geoTiff, chunks={'band': 1, 'x': xchunk, 'y': ychunk})
    da = xarray.open_rasterio(geoTiff, chunks={'band': 1, 'y': ychunk, 'x': xchunk})

    
    #these are just relative to the first scene - not accurate for ALL scenes
    # rows = xpart.rows
    # cols = xpart.cols

    rows, cols = _get_actual_rows_cols(geoTiff, xpart.bbox)

    frow0 = rows[0]
    frow1 = rows[1]

    fcol0 = cols[0]
    fcol1 = cols[1]

    # fudge this for now
    if ((fcol1 - fcol0) > xpart.width):
        fcol1 = fcol1 - 1

    if ((frow1 - frow0) > xpart.height):
        frow1 = frow1 - 1

    if ((fcol1 - fcol0) < xpart.width):
        fcol1 = fcol1 + 1

    if ((frow1 - frow0) < xpart.height):
        frow1 = frow1 + 1


    
    # # print(da)
    my_raster = da.sel(band=1)
   
    # print(my_raster.shape)
    # print(rows[0], rows[1])
    #holding_tank = my_raster[rows[0]:rows[1], cols[0]:cols[1]]
    holding_tank = my_raster[frow0:frow1, fcol0:fcol1]

    # with rasterio.open(geoTiff)as src:
        # w = src.read(1, window=rasterio.windows.Window(cols[0], rows[0], xpart.width, xpart.height))
    # print("W",w.shape)
    #databuf = my_raster[rows[0]:rows[1], cols[0]:cols[1]]
    # print("dat shape", databuf.shape)
    #tank_holding = numpy.flip(holding_tank)
    #tank_holding = numpy.swapaxes(holding_tank,0,1)
    #numpy.copyto(databuf,tank_holding)

    numpy.copyto(databuf,holding_tank)
    #numpy.copyto(databuf,w)
   



def build_the_xarray(geojson, measures, df):

    redfile = df.iloc[0]['red']
    xpart = Xpart(geojson, redfile)

    print(xpart.width)
    print(xpart.height)
    print(xpart.rows)
    print(xpart.cols)

    # return ("BOMB!")

    THE_XARRAY = _build_the_xarray(xpart, measures, df)
    return THE_XARRAY



def _build_the_xarray(xpart, measures, df):
    data = {}
    THE_XARRAY = xarray.Dataset(attrs={'crs': xpart.crs})
    
    # print(THE_XARRAY)
    time_coords = []
    date_coords = []
    for idx, val in df.iterrows():
        key = val['date'] + '_' + val['path'] + '_' + val['row']
        # print (key)
        time_coords.append(key)
        date_coords.append(val['date'])
    
    THE_XARRAY['datePR'] = time_coords
    THE_XARRAY['time'] = date_coords
    # print(THE_XARRAY)
    
    #print(geobox.coordinates.items())
    
    THE_XARRAY['y'] = ('y', xpart.ys, {'units': 'metres'})
    THE_XARRAY['x'] = ('x', xpart.xs, {'units': 'metres'})

    #for name, coord in geobox.coordinates.items():
            #THE_XARRAY[name] = (name, coord.values, {'units': coord.units})
            # print("GN=",name)
            # print(name, len(coord.values))
            # print(name, coord.values[0])
    # print(THE_XARRAY)
    
    print ("TONY len of time_coords", len(time_coords))
    # sys.exit(0)
    datePR_shape = (len(time_coords), )
    
    for color in measures:
        total_shape = datePR_shape + xpart.shape
        # total_shape = datePR_shape + xpart.numpy_shape
        print("total_shape =", total_shape)
        data[color] = numpy.full(total_shape, '-9999', dtype='int16')
        # data[color] = numpy.full(datePR_shape + xpart.shape, '-9999', dtype='int16')
        # data[color] = numpy.full(datePR_shape + xpart.numpy_shape, '-9999', dtype='int16')

        # print("color data.shape", color, data[color].shape)
    
        attrs = {
                    'nodata': '-9999',
                    'units': 'metres',
                    'crs': xpart.crs
                }

    #dims = 'datePR' + tuple(geobox.dimensions)
    
        #dims = ('datePR', 'x', 'y')
        dims = ('datePR', 'y', 'x')
    
        THE_XARRAY[color] = (dims, data[color], attrs)
        # we NOW have an EMPTY XARRAY
        # print(THE_XARRAY)
    
        for index in range(0,len(time_coords)):
            print("INDEX=",index,color)
            read_data_from_geotiff(data[color][index], index, color, xpart, df)
    
        # print(THE_XARRAY)
        
    return THE_XARRAY


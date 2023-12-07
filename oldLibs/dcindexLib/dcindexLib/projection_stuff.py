""" get the epsg from the tiff file """

from osgeo import gdal,osr


def get_projection_info(tif_file):
    print("HEY get_projection_info:", tif_file)

    ds=gdal.Open(tif_file)
    prj=ds.GetProjection()
    # print (prj)

    epsg = prj.split('AUTHORITY')[-1]
    epsg = epsg.split('"')[-2]

    print(epsg)
    print("---" * 30)
    
    srs=osr.SpatialReference(wkt=prj)
    if srs.IsProjected:
        print (srs.GetAttrValue('projcs'))
    print (srs.GetAttrValue('geogcs'))

    spatial_ref = 'epsg:' + epsg
    return spatial_ref

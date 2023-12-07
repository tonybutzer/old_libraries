""" Generic prepare script library - needs work 
However puttng it in a new file is a start
"""

def make_rules(index, product_list):
    """ I have never understood what this function does and it may have been axed by ODC developers """
    # all_product_names = [prod.name for prod in index.products.get_all()]
    # rules = parse_match_rules_options(index, None, all_product_names, True)
    # all_product_names = ['ls8_level1']

    all_product_names = product_list
    rules = parse_match_rules_options(index, None, all_product_names,True)
    return rules


bands_ls8_espa = [('1', 'sr_band1'),
             ('2', 'blue'),
             ('3', 'green'),
             ('4', 'red'),
             ('5', 'nir'),
             ('6', 'swir1'),
             ('7', 'swir2'),
             ('8', 'therm'),
             ('9', 'pixel_qa')]

band_file_map = {
                  'sr_band1' : 'sr_band1',
                  'blue' : 'sr_band2',
                  'green' : 'sr_band3',
                  'red' : 'sr_band4',
                  'nir' : 'sr_band5',
                  'swir1' : 'sr_band6',
                  'swir2' : 'sr_band7',
                  'therm' : 'bt_band10',
                  'pixel_qa' : 'pixel_qa',
                }

def satellite_ref(sat):
    """
    load the band_names for referencing LANDSAT8  USARD
    """
    if sat == 'LANDSAT_8':
        sat_img = bands_ls8_espa
        prod_type = 'espa'
    else:
        raise ValueError('Satellite data Not Supported')
    return sat_img, prod_type

def get_band_file_map(item):
    return band_file_map[item]

def add_dataset(doc, uri, rules, index):
    """ add a single dataset to the postgresql index 

        1. call create_dataset(datacube) to build the dataset object with the newly created json doc
        2. call index.datasets.add with the dataset document object to populate the DB

    """

    dataset = create_dataset(doc, uri, rules)

    try:
        index.datasets.add(dataset, sources_policy='skip')
    except changes.DocumentMismatchError as e:
        index.datasets.update(dataset, {tuple(): changes.allow_any})
    return uri


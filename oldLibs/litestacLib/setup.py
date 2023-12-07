
from setuptools import setup

setup(name='litestacLib',
      maintainer='Tony Butzer',
      maintainer_email='tonybutzer@gmail.com',
      version='1.0.1',
      description='helper functions for processing an espa order',
      packages=[
          'litestacLib',
      ],
      install_requires=[
          'sat-stac == 0.1.3',
          'sat-search == 0.2.1',
          'pandas',
          'rasterio',
          'xarray',
          'geojson',
          'pyproj',
          'pygeoj',
      ],

      )

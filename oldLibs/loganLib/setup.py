
from setuptools import setup

setup(name='loganLib',
      maintainer='Logan M',
      maintainer_email='logan@gmail.com',
      version='1.0.1',
      description='helper functions for invasive data wrangling',
      packages=[
          'loganLib',
      ],
      install_requires=[
          'xarray',
          'folium',
          'shapely',
          'pyproj',
      ],

      )

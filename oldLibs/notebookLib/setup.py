
from setuptools import setup

setup(name='notebookLib',
      maintainer='Tony Butzer',
      maintainer_email='tonybutzer@gmail.com',
      version='1.0.1',
      description='helper functions for processing an espa order',
      packages=[
          'notebookLib',
      ],
      install_requires=[
          'matplotlib',
          'shapely',
          'scikit-image',
          'geopandas',
          'ffmpeg',
      ],

      )

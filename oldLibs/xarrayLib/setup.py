
from setuptools import setup

setup(name='xarrayLib',
      maintainer='Tony Butzer',
      maintainer_email='tonybutzer@gmail.com',
      version='1.0.1',
      description='helper functions for processing an espa order',
      packages=[
          'xarrayLib',
      ],
      install_requires=[
          'affine',
          'boto3',
          'dask',
          'toolz',
      ],

      )

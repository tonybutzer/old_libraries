# Datacube Indexing

- is complicated
- can be avoided using STAC
- can be simplified using elastic search instead of postgresql

## General Flow

for all objects in [localDirectoryTree || bucketPrefix]:
	determine input type from [MTL || xml || json]
	convert to blob of metadata
	store the metadata[blob] in [elastic search || postgresql]

## Software Modules/Files

1. api files - main loop callables for various needs
	- ix_api_elastic.py
	- ix_api_postgres.py  -- ### COMING SOON ###
2. meta_lib files
	- these parse the file into a dict then use the metablob for the type to create a metatdata blob
3. meta_blob
	- these output a universal metablob from each specific type

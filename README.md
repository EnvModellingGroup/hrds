![logo](https://github.com/EnvModellingGroup/hdrs/blob/master/docs/logo_small.png)

About hrds
===========
hrds is a python package for obtaining points from a set of raster at different resolutions.
You can request a point (or list of points) and hrds will return a value based on
the highest resolution dataset (as defined by the user) available at that point, blending
datasets in a buffer region to ensure consistancy.

Prerequisites
---------------
* python 2.7
* numpy
* scipy
* osgeo.gdal to read and write raster data

Functionality
---------------
* Create buffer zones as a preprocessing step
* Obtain value at a point or list of points based on user-defined priority of rasters


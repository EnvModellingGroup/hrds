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
* to read from netCDF sources: python netCDF support. The
[netCDF4](https://github.com/Unidata/netcdf4-python) package is 
recommended. To install:
```
sudo CC=mpicc pip install netcdf4
```
or use the python-netcdf4 package on Ubuntu and Debian.

Functionality
---------------
* Create buffer zones as a preprocessing step
* Obtain value at a point or list of points based on user-defined priority of rasters


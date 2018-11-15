![logo](https://github.com/EnvModellingGroup/hdrs/blob/master/docs/logo_small.png)

About hrds
===========
hrds is a python package for obtaining points from a set of raster at 
different resolutions.
You can request a point and hrds will return a value based on
the highest resolution dataset (as defined by the user) available at that point, blending
datasets in a buffer region to ensure consistancy.

Prerequisites
---------------
* python 2.7 or 3.
* numpy
* scipy
* osgeo.gdal to read and write raster data

To install pygdal, install the libgdal-dev packages and binaries, e.g.

```bash
sudo apt-get install libgdal-dev gdal-bin
```

Then check which version is installed:
```bash
gdal-config --version
```

Install using pip, the correct version. Note you may need to 
increase the minor version number, e.g. from 2.1.3 to 2.1.3.3

```bash
pip install pygdal==2.1.3
```

To use this in your Firedrake environment, remember to do the last step after
activating the Firedrake environment.

Functionality
---------------
* Create buffer zones as a preprocessing step if needed
* Obtain value at a point based on user-defined priority of rasters

Example of use via [thetis](http://thetisproject.org/):
```python
from firedrake import *
from thetis import *
from firedrake import Expression
import sys
sys.path.insert(0,"../../")
from hrds import HRDS

mesh2d = Mesh('test.msh') # mesh file

P1_2d = FunctionSpace(mesh2d, 'CG', 1)
bathymetry2d = Function(P1_2d, name="bathymetry")
bvector = bathymetry2d.dat.data
bathy = HRDS("gebco_uk.tif", 
             rasters=("emod_utm.tif", 
                      "marine_digimap.tif"), 
             distances=(10000, 5000))
bathy.set_bands()
for i, (xy) in enumerate(mesh2d.coordinates.dat.data):
    bvector[i] = bathy.get_val(xy)
File('bathy.pvd').write(bathymetry2d)
```

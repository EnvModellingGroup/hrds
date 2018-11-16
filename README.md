
![logo](https://github.com/EnvModellingGroup/hdrs/blob/master/docs/logo_small.png)

About hrds
===========
hrds is a python package for obtaining points from a set of rasters at 
different resolutions.
You can request a point and hrds will return a value based on
the highest resolution dataset (as defined by the user) available at that point, blending
datasets in a buffer region to ensure consistency.

[![Build Status](https://travis-ci.org/EnvModellingGroup/hdrs.svg?branch=master)](https://travis-ci.org/EnvModellingGroup/hdrs)

Prerequisites
---------------
* python 2.7 or 3.
* numpy
* scipy
* osgeo.gdal (pygdal) to read and write raster data

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

You can install HRDS using the standard:
```bash
python setup.py install
```

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

This example loads in an XYZ file and obtains data at each point, 
replacing the Z value with that from HRDS.

```python
from hrds import HRDS

points = []
with open("test.xyz",'r') as f:
    for line in f:
        row = line.split()
        # grab X and Y
        points.append([float(row[0]), float(row[1])])

bathy = HRDS("gebco_uk.tif", 
             rasters=("emod_utm.tif", 
                      "marine_digimap.tif"), 
             distances=(10000, 5000))
bathy.set_bands()

with open("output.xyz","w") as f:
    for p in points:
        f.write(str(p[0])+"\t"+str(p[1])+"\t"+str(bathy.get_val(p))+"\n")

```

This will turn this:
```bash
$ head test.xyz 
778000 5960000 0
778000 5955006.00490137 0
778000 5950012.00980273 0
778000 5945018.0147041 0
778000 5940024.01960546 0
778000 5935030.02450683 0
778000 5930036.02940819 0
778000 5925042.03430956 0
778000 5920048.03921092 0
778000 5915054.04411229 0
```

into this:

```bash
$ head output.xyz 
778000.0	5960000.0	-23.2977278648
778000.0	5955006.0049	-16.3622326359
778000.0	5950012.0098	-17.8316399298
778000.0	5945018.0147	-12.1837755526
778000.0	5940024.01961	-17.2785563521
778000.0	5935030.02451	-13.0309790235
778000.0	5930036.02941	-11.081550282
778000.0	5925042.03431	-8.37494903047
778000.0	5920048.03921	-18.8159019752
778000.0	5915054.04411	-17.9226424001
```

These images show the original data in QGIS (note the "edges" between rasters,
higlighted by the arrows in the right 
hand close-up). The figure also shows the buffer regions created around the 
two higher resolution datasets (bottom left). The red line is the boundary of the
mesh used (see figure below).


![Input data](https://github.com/EnvModellingGroup/hdrs/blob/master/docs/original_bathy_data_sml.png)

After running the code above, we produce this blended dataset. The mesh is shown in the 
lower left, with a close-up on the right. Mesh varied in resolution from 
2000m to 50m. Note the three bathymetric highs (yellow) near the Gebco label above
are smoothed in the buffer region and there is no longer the obvious line
between the Gebco data and the EMod data.

![Blended bathymetry data on the multiscale mesh](https://github.com/EnvModellingGroup/hdrs/blob/master/docs/blended_rasters_with_mesh_sml.png)

Community
-----------

We welcome suggestions for future improvements, bug reports and other issues via the issue tracker. Anyone wishing to contribute code should contact Jon Hill (jon.hill@york.ac.uk) to discuss.


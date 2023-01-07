import firedrake
import thetis
from hrds import HRDS

mesh2d = firedrake.Mesh('test_mesh.msh') # mesh file

min_coords = np.amin(mesh2d.coordinates.dat.data_ro, axis=0)
max_coords = np.amax(mesh2d.coordinates.dat.data_ro, axis=0))

P1_2d = firedrake.FunctionSpace(mesh2d, 'CG', 1)
bathymetry2d = firedrake.Function(P1_2d, name="bathymetry")
bvector = bathymetry2d.dat.data
bathy = HRDS("gebco_uk.tif", 
             rasters=("emod_utm.tif", 
                      "inspire_data.tif"), 
             distances=(700, 200))
bathy.set_bands()
for i, (xy) in enumerate(mesh2d.coordinates.dat.data):
    bvector[i] = bathy.get_val(xy)
thetis.File('bathy.pvd').write(bathymetry2d)





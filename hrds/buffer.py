import numpy as np
from osgeo import gdal
import math
from raster import RasterInterpolator
from scipy.ndimage.morphology import distance_transform_edt

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Copyright Jon Hill, University of York, jon.hill@york.ac.uk

# read in a raster and create the buffer from 0 at edge, to 1 at distance

filename = "../tests/test_raster_large.tif"
raster = RasterInterpolator(filename)
raster.set_band()
extent = raster.get_extent()

# make a raster of the same extent, but with
# square resolution which is dependant on distance buffer
distance = 1.5 # in same units are raster
# we want 10 pixels to cover the distance, so...
dx = distance / 10.0
llc = extent[1]
urc = extent[3]
# note this changes our extent
nrows = int((urc[0] - llc[0]) / dx) + 1
ncols = int((urc[1] - llc[1]) / dx) + 1

print dx, llc, urc, nrows, ncols

# fill with edge value
dist = np.full((nrows,ncols),0,dtype=np.uint8)
# then fill in the middle
dist[1:-1,1:-1] = 1
# calc euclidian distance and convert to units
dist = distance_transform_edt(dist)*dx
# now make it 0 -> 1
dist = dist / distance
dist[dist > 1] = 1.0

print dist

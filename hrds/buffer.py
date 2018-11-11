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

def write_raster(filename, array, dx, origin, proj):
    dst_filename = filename
    x_pixels = array.shape[0]
    y_pixels = array.shape[1]     
    x_min = origin[0][0]
    y_max = origin[1][1]
    wkt_projection = proj

    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(
        dst_filename,
        x_pixels,
        y_pixels,
        1,
        gdal.GDT_Float32, )

    print x_min, y_max, dx

    dataset.SetGeoTransform((
        x_min,       # 0
        dx,          # 1
        0,           # 2
        y_max,       # 3
        0,           # 4
        -dx))  

    dataset.SetProjection(wkt_projection)
    dataset.GetRasterBand(1).WriteArray(array)
    dataset.FlushCache()
    return

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

write_raster('test.tif',dist, dx, [llc,urc],raster.ds.GetProjection())

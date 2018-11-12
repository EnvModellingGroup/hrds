import numpy as np
from osgeo import gdal
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


class CreateBuffer(object):
    """Implements the creation of a distance buffer from the edge of
    a raster to the centre:

    rbuff = CreateBuffer('myRaster.tif',10000.0)

    Will create a buffer raster with the same extents as myRaster.tif
    with a buffer that goes from 0 at the edge to 1.0 at a distance of
    10,000 units from the edge. The distance should be in the same
    units as the raster file.

    Once the object is made, write out the buffer using:

    rbuff.make_buffer('output_buffer.tif')

    Any GDAL-understood file format is supported for input or output.

    The array is stored at an 8-bit integer internally and converted to
    a 32 bit float on writing.
    """

    def __init__(self, filename, distance, over=10.0):

        self.distance = distance
        self.over = over
        self.raster = RasterInterpolator(filename)
        self.raster.set_band()
        self.extent = self.raster.get_extent()

    def __write_raster__(self, filename, array, dx, origin, proj):
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
            gdal.GDT_Float32)

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

    def make_buffer(self, output_file):
        # make a raster of the same extent, but with
        # square resolution which is dependant on distance buffer

        dx = self.distance / self.over
        llc = self.extent[1]
        urc = self.extent[3]
        # note this changes our extent
        nrows = int((urc[0] - llc[0]) / dx) + 1
        ncols = int((urc[1] - llc[1]) / dx) + 1

        # fill with edge value
        dist = np.full((nrows, ncols), 0, dtype=np.uint8)
        # then fill in the middle
        dist[1:-1, 1:-1] = 1
        # calc euclidian distance and convert to units
        dist = distance_transform_edt(dist) * dx
        # now make it 0 -> 1
        dist = dist / self.distance
        dist[dist > 1] = 1.0

        # create a suitable output filename
        self.__write_raster__(output_file, dist, dx, [llc, urc],
                              self.raster.ds.GetProjection())

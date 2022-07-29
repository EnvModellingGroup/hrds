import numpy as np
from osgeo import gdal
from .raster import RasterInterpolator
from scipy.ndimage.morphology import distance_transform_edt
from math import ceil

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


class CreateBuffer():
    """
    Implements the creation of a distance buffer from the edge of
    a raster to the centre::

        rbuff = CreateBuffer('myRaster.tif',10000.0)

    Will create a buffer raster with the same extents as myRaster.tif
    with a buffer that goes from 0 at the edge to 1.0 at a distance of
    10,000 units from the edge. The distance should be in the same
    units as the raster file.

    You can also specify the "resolution" of your buffer using the 'over'
    argument. Using '10' would use ten units resolve the buffer from
    edge to distance (e.g. is distance was 1.5, and over was 10, your output
    buffer would have a dx of 0.15). This will probably alter the extents
    of your buffer raster such that it no longer matches the actual raster,
    so proceed with caution. It may however, be useful if your input raster
    has very high resolution and you want to prevent multiple large raster
    files.

    Once the object is made, write out the buffer using::

        rbuff.make_buffer('output_buffer.tif')

    Any GDAL-understood file format is supported for input or output.
    """

    def __init__(self, filename, distance, over=None):
        """
        Init our buffer

        Args:
            filename: filename to write to
            distance: distance (in raster units) to extend buffer over
            over: alter the distance to be in some other units

        Returns:
            a createBuffer object
        """
        self.distance = distance
        self.over = over
        self.raster = RasterInterpolator(filename)
        self.raster.set_band()
        self.extent = self.raster.get_extent()

    def __write_raster__(self, filename, array, dx, origin, proj):
        """
        Write raster to file

        Args:
            filename: filename to write to
            array: the data. 2D numpy array
            dx: resolution (length 2 list)
            origin: the LLC coordinates
            proj: Projection space for the raster (wkt)

        Returns:
            Nothing
        """
        dst_filename = filename
        x_pixels = array.shape[1]
        y_pixels = array.shape[0]
        x_min = origin[0][0]
        y_max = origin[0][1] + dx[1]*y_pixels
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
            dx[0],       # 1
            0,           # 2
            y_max,       # 3
            0,           # 4
            -dx[1]))

        dataset.SetProjection(wkt_projection)
        dataset.GetRasterBand(1).WriteArray(array)
        dataset.FlushCache()
        return

    def extend_mask(self, array, iterations):
        """
        Extend the mask a number of "cells" in all directions"

        Args:
            array: the numpy aray to extend
            iterations: integer for how many cells to extend

        Returns:
            a numpy array
        """

        # function to extend a mask array.
        # Taken from: http://www.siafoo.net/snippet/82
        # Copyright 2007 Regents University of California
        # Written by David Isaacson under BSD licence
        yLen, xLen = array.shape
        output = array.copy()
        for i in range(iterations):
            for y in range(yLen):
                for x in range(xLen):
                    if (y > 0 and array[y-1, x]) or \
                       (y < yLen - 1 and array[y+1, x]) or \
                       (x > 0 and array[y, x-1]) or \
                       (x < xLen - 1 and array[y, x+1]):
                        output[y, x] = True
            array = output.copy()

        return output

    def make_buffer(self, output_file):
        """
        Create a buffer raster from 0 to 1 over a set distance.

        Args:
            output_file: where to save this raster
        """

        # make a raster of the same extent, but with
        # square resolution which is dependant on distance buffer

        llc = self.extent[1]
        urc = self.extent[3]
        if self.over is None:
            transform = self.raster.ds.GetGeoTransform()
            dx = [transform[1], -transform[5]]
            nrows = self.raster.ds.RasterXSize
            ncols = self.raster.ds.RasterYSize
        else:
            dx = [self.distance / self.over, self.distance / self.over]
            # note this changes our extent if "over" is set
            nrows = int(ceil((urc[0] - llc[0]) / dx[0]))
            ncols = int(ceil((urc[1] - llc[1]) / dx[1]))

        # fill with edge value
        dist = np.full((ncols, nrows), 0.0)
        # then fill in the middle,
        # except where there is no data
        dist[1:-1, 1:-1] = 1
        if self.over is None:
            orig_raster = self.raster.get_array()
            nodata = self.raster.nodata
            # TODO this will only work if dist and orig_raster
            # are the same size
            dist[orig_raster == nodata] = 0
            # they also be nan...(shouldn't as we swap it out...)
            dist[np.isnan(orig_raster)] = 0
            # we now extend this mask - we only need to do this, if the
            # no data occurs (i.e. no contiguous data)
            if (nodata in orig_raster):
                mask = np.full((ncols, nrows), False)
                mask[dist == 0] = True
                mask = self.extend_mask(mask, 1)
                dist[mask] = 0
        # calc euclidian distance and convert to 0 -> 1 scale
        dist = distance_transform_edt(dist, sampling=[dx[0], dx[1]])
        dist = dist / self.distance
        dist[dist > 1] = 1.0

        # create a suitable output filename
        self.__write_raster__(output_file, np.flipud(dist), dx, [llc, urc],
                              self.raster.ds.GetProjection())

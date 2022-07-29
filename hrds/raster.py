import numpy as np
from osgeo import gdal
import math

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

"""
This module contains the Interpolator class and the RasterInterpolator
class. These RasterInterpolator class reads in a GDAL raster and
then allows interagation of that data at an arbitrary point using
bi-linear interpolation.
"""


class RasterInterpolatorError(Exception):
    """
    A generic error created by the RasterInterpolator class
    """

    pass


class CoordinateError(RasterInterpolatorError):
    """
        Raised when a point is outside the raster or the land mask
    """
    def __init__(self, message, x, i, j):
        self.message = message
        self.x = x
        self.ij = i, j

    def __str__(self):
        return "at x, y={} indexed at i, j={}; {}".format(self.x, self.ij,
                                                          self.message)


class Interpolator():
    """Implements an object to interpolate values from a Raster-type data set.

    Used by the RasterInterpolator. A separate object as in the future we
    may switch bands and hence have to reload the val data.
    """

    def __init__(self, origin, delta, val, mask=None, minmax=None):
        """
        Init our Interpolator

        Args:
            origin: where the raster starts (LLC)
            delta: resolution (length 2 list [dx,dy])
            val: 2D numpy array of data
            mask: a land mask (not yet implemented)
            minmax: any min/max values to adhere to (length 2 list [min,max])

        Returns:
            a Interpolator object
        """
        self.origin = origin
        self.delta = delta
        self.val = val
        self.mask = mask
        self.minmax = minmax

    def set_mask(self, mask):
        """
        Set a mask to use. Not yet implemented.
        """
        self.mask = mask

    def get_val(self, point):
        """
        Get the value of this raster at the desired point via bi-linear
        interpolation.

        Args:
            point: a length 2 list containing x,y coordinates

        Returns:
            The value of the raster stack at that point

        Raises:
            CoordinateError: The point is outside the rasters
            RasterInterpolatorError: Generic error interpolating data at
                that point
        """

        yhat = ((point[0]+(self.delta[0]/2.0)-self.origin[0])/self.delta[0])
        xhat = ((point[1]+(self.delta[1]/2.0)-self.origin[1])/self.delta[1])
        j = int(math.floor(yhat))-1
        i = int(math.floor(xhat))-1
        # this is not caught as an IndexError below, because of wrapping of
        # negative indices
        if i < 0 or j < 0:
            raise CoordinateError("Coordinate out of range", point, i, j)
        alpha = (xhat) % 1.0
        beta = (yhat) % 1.0
        neigh_i = i+1
        neigh_j = j+1
        if neigh_i < 0 or neigh_j < 0:
            raise CoordinateError("Coordinate out of range", point, i, j)
        try:
            if self.mask is not None:
                # case with a land mask - masks not yet implemented!
                w00 = (1.0-alpha)*(1.0-beta)*self.mask[i, j]
                w10 = alpha*(1.0-beta)*self.mask[i+1, j]
                w01 = (1.0-alpha)*beta*self.mask[i, j+1]
                w11 = alpha*beta*self.mask[i+1, j+1]
                if len(self.val.shape) == 2:
                    value = w00*self.val[i, j] + w10*self.val[i+1, j] \
                            + w01*self.val[i, j+1] + w11*self.val[i+1, j+1]
                else:
                    raise RasterInterpolatorError("Field to interpolate,"
                                                  "should have 2 dimensions")
                sumw = w00+w10+w01+w11

                if sumw > 0.0:
                    value = value/sumw
                else:
                    raise CoordinateError("Probing point inside land mask",
                                          point, i, j)

            else:
                # case without a land mask
                if len(self.val.shape) == 2:
                    value = ((1.0-beta)*((1.0-alpha)*self.val[i, j] +
                                         alpha*self.val[neigh_i, j]) +
                             beta*((1.0-alpha)*self.val[i, neigh_j] +
                                   alpha*self.val[neigh_i, neigh_j]))
                else:
                    raise RasterInterpolatorError("Field to interpolate,"
                                                  "should have 2 dimensions")
        except IndexError:
            raise CoordinateError("Coordinate out of range", point, i, j)

        if self.minmax is not None:
            if self.minmax[0] is not None:
                if value < self.minmax[0]:
                    value = self.minmax[0]
            if self.minmax[1] is not None:
                if value > self.minmax[1]:
                    value = self.minmax[1]

        return value


# note that a RasterInterpolator is *not* object an Interpolator object
# the latter is considered immutable, whereas the NetCDFInterpolator may
# change in future
class RasterInterpolator(object):
    """
    Implements an object to interpolate values from a Raster-stored data set::

        rci = RasterInterpolator('foo.tif')

    Any GDAL supported raster format should be fine. The origin is assumed
    to be the lower-left corner (i.e. south west)
    and the projection space is stored with the raster.

    To indicate the band to be interpolated::

        rci.set_band(2)

    The default is Band 1 (ie. with no number given)

    To interpolate this field in any arbitrary point::

        rci.get_val((-3.0, 58.5))

    It is allowed to switch between different fields using multiple
    calls of set_band().

    """
    def __init__(self, filename, minmax=None):
        """
        Init our RasterInterpolator

        Args:
            filename: Which raster to load
            minmax: any min/max values to adhere to (length 2 list [min,max])

        Returns:
            a RasterInterpolator object
        """
        self.ds = gdal.Open(filename)
        if (self.ds is None):
            raise RasterInterpolatorError("Couldn't find your raster file:" +
                                          filename + ". Exiting.")
        self.band = None
        self.mask = None
        self.interpolator = None
        self.extent = None
        self.dx = 0.0
        self.nodata = None
        self.minmax = minmax

    def get_extent(self):
        """Return list of corner coordinates from a geotransform

        Returns:
            List continaing the corner coordinates of the raster

        """
        cols = self.ds.RasterXSize
        rows = self.ds.RasterYSize
        gt = self.ds.GetGeoTransform()

        ext = []
        xarr = [0, cols]
        yarr = [0, rows]

        for px in xarr:
            for py in yarr:
                x = gt[0] + (px * gt[1]) + (py * gt[2])
                y = gt[3] + (px * gt[4]) + (py * gt[5])
                ext.append([x, y])
            yarr.reverse()
        return ext

    def set_band(self, band_no=1):
        """
        Set the number of the band to be used. Usually 1, which is default

        Args:
            band_no: an integer which is the band number to use. Default is 1.

        """
        self.band = band_no
        raster = self.ds.GetRasterBand(self.band)
        self.nodata = raster.GetNoDataValue()
        self.val = np.flipud(np.array(raster.ReadAsArray()))
        # fix any NAN with the no-data value
        if (np.isnan(self.val).any()):
            self.val[np.isnan(self.val)] = self.nodata
        self.extent = self.get_extent()
        origin = np.amin(self.extent, axis=0)
        transform = self.ds.GetGeoTransform()
        self.dx = [transform[1], -transform[5]]
        self.interpolator = Interpolator(origin, self.dx, self.val,
                                         self.mask, self.minmax)

    def get_array(self):
        """
        Get the raw data in the raster

        Returns:
            a numpy array containing the raster data
        """
        if (self.interpolator is None):
            raise RasterInterpolatorError("Should call set_band() "
                                          "before calling get_array()!")
        return self.val

    def get_val(self, x):
        """
        Interpolate the field chosen with set_field().
        The order of the coordinates should correspond
        with the storage order in the file.

        Args:
            point: a length 2 list containing x,y coordinates

        Returns:
            The value of the raster stack at that point

        Raises:
            CoordinateError: The point is outside the rasters
            RasterInterpolatorError: Generic error interpolating
                data at that point

        """
        if (self.interpolator is None):
            raise RasterInterpolatorError("Should call set_band() "
                                          "before calling get_val()!")
        val = self.interpolator.get_val(x)
        return val

    def point_in(self, point):
        """
        Does a point lay inside a raster's extent?

        Args:
            point: a length 2 list containing x,y coordinates

        Returns:
            Boolean. True if point is in the raster. False otherwise.
        """

        # does this point occur in the raster?
        llc = np.amin(self.extent, axis=0)+(self.dx[0]/2)
        urc = np.amax(self.extent, axis=0)-(self.dx[1]/2)
        if ((point[0] <= urc[0] and point[0] >= llc[0]) and
           (point[1] <= urc[1] and point[1] >= llc[1])):
            return True
        else:
            return False

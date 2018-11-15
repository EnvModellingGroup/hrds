from .raster import RasterInterpolator
from .raster_buffer import CreateBuffer
import os
try:
    from itertools import izip as zip
except ImportError: # will be 3.x series
    pass
from __future__ import print_function

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

# create a heirachy of rasters to pull data from, smoothly blending
# between them


class HRDS(object):

    def __init__(self, baseRaster, rasters=None, distances=None, buffers=None):
        """ baseRaster is the low res raster filename across whole domain.
        rasters is a list of filenames of the other rasters in priority order.
        distances is the distance to create a buffer (in same units as
        corresponding raster) for each.
        buffers is a lost of buffer filenames in the same order,
        if created already.
        """

        # TODO some basic checks, such as length of all arguments here
        self.baseRaster = RasterInterpolator(baseRaster)
        self.raster_stack = []
        for r in rasters:
            self.raster_stack.append(RasterInterpolator(r))
        self.buffer_stack = []
        if buffers is None:
            for r, d in zip(rasters, distances):
                # create buffer file name, based on raster filename
                buf_file = os.path.splitext(r)[0]+"_buffer.tif"
                # create buffer
                rbuff = CreateBuffer(r, d)
                rbuff.make_buffer(buf_file)
                # add to stack
                self.buffer_stack.append(RasterInterpolator(buf_file))
        else:
            # create buffer stack from filenames
            for r in buffers:
                self.buffer_stack.append(RasterInterpolator(r))

        # reverse the arrays
        self.buffer_stack.reverse()
        self.raster_stack.reverse()

    def set_bands(self, bands=None):

        if bands is None:
            self.baseRaster.set_band()
            for r in self.raster_stack:
                r.set_band()
            for r in self.buffer_stack:
                r.set_band()
        else:
            counter = 1
            self.baseRaster.bands(bands[0])
            for r in self.raster_stack:
                r.set_band(bands[counter])
                counter += 1
            counter = 1
            for r in self.buffer_stack:
                r.set_band(bands[counter])
                counter += 1

    def get_val(self, point):
        # the actual meat of this code!
        # determine if we're in any of the rasters in the list,
        # starting from the last one
        for i, r, b in zip(range(0, len(self.raster_stack)+1),
                           self.raster_stack,
                           self.buffer_stack):
            if r.point_in(point):
                # if so, check the buffer value
                if b.get_val(point) == 1.0:
                    return r.get_val(point)
                else:
                    for rr in self.raster_stack[i+1:]:
                        # if not, find the next raster we're in, inc. the base
                        if rr.point_in(point):
                            val = r.get_val(point)*b.get_val(point) + \
                                  rr.get_val(point)*(1-b.get_val(point))
                            return val
                    # if we get here, there is no other layer,
                    # so use base raster
                    val = r.get_val(point)*b.get_val(point) + \
                        self.baseRaster.get_val(point)*(1-b.get_val(point))
                    return val

        # we're not in the raster stack, so return value from base
        return self.baseRaster.get_val(point)

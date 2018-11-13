import unittest
from hrds.raster import RasterInterpolator, CoordinateError, RasterInterpolatorError
import itertools
import os
from numpy import arange, array, ones

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

test_file_name1 = "tests/test_raster.asc"

class TestRasterInterpolator(unittest.TestCase):
    """Tests the hrds.raster.RasterInterpolator class"""
    def setUp(self):
        return

    def tearDown(self):
        return
    
    def test_simple_interpolation(self):
        """ Very simple test with a raster object like thus:
             1  2  3  4
             5  6  7  8
             9  10 11 12
             13 14 15 16
            
            LLC is 0,0 and upper right is 4,4. 
            The data are stored in cell centres and we ask for a few coords
            """
        rci = RasterInterpolator(test_file_name1)
        point1 = [0.0, 0.0] # should error
        point2 = [1.5, 2.0] # should return 8
        point3 = [2.0, 3.0] # should return 4.5
        point4 = [3,1] # should return 13.5
        point5 = [1.999999, 2.999999] # should return nearly 4.5
        self.assertRaises(RasterInterpolatorError, rci.get_val, point2)
        rci.set_band()        
        self.assertEqual(rci.get_val(point2),8.0)
        self.assertAlmostEqual(rci.get_val(point3),4.5)
        self.assertAlmostEqual(rci.get_val(point5),4.5,5)
        self.assertEqual(rci.get_val(point4),13.5)
        self.assertRaises(CoordinateError,rci.get_val, point1)



if __name__ == '__main__':
    unittest.main()

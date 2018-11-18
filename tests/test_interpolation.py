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
        point6 = [0.5, 0.5] # should return 13 (llc)
        self.assertRaises(RasterInterpolatorError, rci.get_val, point2)
        rci.set_band()        
        self.assertEqual(rci.get_val(point2),8.0)
        self.assertAlmostEqual(rci.get_val(point3),4.5)
        self.assertAlmostEqual(rci.get_val(point5),4.5,5)
        self.assertEqual(rci.get_val(point4),13.5)
        self.assertEqual(rci.get_val(point6),13)
        self.assertRaises(CoordinateError,rci.get_val, point1)

    def test_point_in(self):
        """ Very simple test with a raster object like thus:
             1  2  3  4
             5  6  7  8
             9  10 11 12
             13 14 15 16
            
            LLC is 0,0 and upper right is 4,4. 
            we ask for point in, outside and on boundary
            """
        rci = RasterInterpolator(test_file_name1)
        point1 = [0.0, 0.0] # should return False
        point2 = [2.0, 2.0] # should return True
        point3 = [-1.0, -1.0] # should return False
        point4 = [0.5, 0.5] # should return True
        point5 = [0.0001, 0.0001] # False - outside first cell centre
        rci.set_band()
        self.assertFalse(rci.point_in(point1))
        self.assertTrue(rci.point_in(point2))
        self.assertFalse(rci.point_in(point3))
        self.assertTrue(rci.point_in(point4))
        self.assertFalse(rci.point_in(point5))

    @unittest.skipUnless(os.path.isfile("tests/real_data/gebco_uk.tif"),
                         "Skipping as proprietary data missing.")
    def test_real_data(self):
        """Using gebco cut out to test interpolation
        """
        raster_file = "tests/real_data/gebco_uk.tif"
        rci = RasterInterpolator(raster_file)
        rci.set_band()
        points = ([823862., 5782011.],
                  [839323., 5782408.],
                  [853000., 5782804.],
                  [858947., 5782606.],
                  [866083., 5783201.],
                  [889870., 5784787.],
                  [949138., 5782408.],
                  )
        expected = [-21.22,
                    -24.03,
                    -38.03,
                    -46.72,
                    -40.01,
                    -32.13,
                    -22.19]
        for p,e in zip(points, expected):
            self.assertAlmostEqual(rci.get_val(p),e,delta=0.75)
        


if __name__ == '__main__':
    unittest.main()

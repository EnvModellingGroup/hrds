import unittest
from hdrs.raster import RasterInterpolator, CoordinateError, RasterInterpolatorError
import itertools
import os
from numpy import arange, array, ones

test_file_name1 = "tests/test_raster.asc"

class TestNetCDFInterpolator(unittest.TestCase):
    """Tests the uptide.netcdf.NetCDFInterpolator class"""
    def setUp(self):
        return

    def tearDown(self):
        # don't remove them either (see above)
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
        point2 = [1.5, 2] # should return 8
        point3 = [2.0, 2.99999999] # should return 4.5
        point4 = [3,1] # should return 13.5
        self.assertRaises(RasterInterpolatorError, rci.get_val, point2)
        rci.set_band()        
        self.assertEqual(rci.get_val(point2),8.0)
        self.assertAlmostEqual(rci.get_val(point3),4.5)
        self.assertEqual(rci.get_val(point4),13.5)
        self.assertRaises(CoordinateError,rci.get_val, point1)



if __name__ == '__main__':
    unittest.main()

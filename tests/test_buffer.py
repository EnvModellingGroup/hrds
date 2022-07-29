import unittest
import os
import sys
# make sure we use the devel version first
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__))+'/..')
from hrds.raster_buffer import CreateBuffer
from hrds.raster import RasterInterpolator, CoordinateError, RasterInterpolatorError

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

test_dir = os.path.split(__file__)[0]

test_file_name1 = os.path.join(test_dir, "test_raster_large.tif")
test_file_name2 = os.path.join(test_dir, "test_raster_nodata_centre.tif")

temp_file = "temp.tif"


class TestBufferCreator(unittest.TestCase):
    """Tests the hrds.buffer.CreateBuffer class"""
    def setUp(self):
        return

    def tearDown(self):
        # remove temp file
        #os.remove(temp_file)
        return

    def test_simple_distance(self):
        """ Very simple test with a raster object like thus:
             1  2  3  4
             5  6  7  8
             9  10 11 12
             13 14 15 16
            (on a 10x10 grid, not 4x4 as above...only so much space
            in comments!)

            LLC is 0,0 and upper right is 4,4. (hence dx is 0.25)
            The data are stored in cell centres and we ask for a few coords.
            We check that the value is 1 at the distance, 0 at the boundary.
            Finally, test that the file is written and readable
            """
        rbuff = CreateBuffer(test_file_name1, 1.5)
        point1 = [0.2, 3.85]  # should return <0.25 (resolution)
        point2 = [1.7, 2]  # should be 1
        point3 = [2, 2]  # should be 1
        point4 = [0.85, 2]  # should be 0.5
        rbuff.make_buffer(temp_file)
        # we now read in the buffer using the rasterinterpolator class
        rci = RasterInterpolator(temp_file)
        rci.set_band()
        self.assertAlmostEqual(rci.get_val(point1), 0.0, delta=0.03)
        self.assertEqual(rci.get_val(point2), 1.0)
        self.assertEqual(rci.get_val(point3), 1.0)
        self.assertAlmostEqual(rci.get_val(point4), 0.5, delta=0.03)

    def test_simple_distance_setres(self):
        """ Very simple test with a raster object like thus:
             1  2  3  4
             5  6  7  8
             9  10 11 12
             13 14 15 16
            (on a 10x10 grid, not 4x4 as above...only so much space
            in comments!)

            LLC is 0,0 and upper right is 4,4. (hence dx is 0.25)
            The data are stored in cell centres and we ask for a few coords.
            We check that the value is 1 at the distance, 0 at the boundary.
            Finally, test that the file is written and readable
            """
        rbuff = CreateBuffer(test_file_name1, 1.5, over=30)
        point1 = [0.03, 3.85]  # should return ~0
        point2 = [1.65, 2]  # should be 1
        point3 = [2, 2]  # should be 1
        point4 = [0.76, 2]  # should be ~0.5
        rbuff.make_buffer(temp_file)
        # we now read in the buffer using the rasterinterpolator class
        rci = RasterInterpolator(temp_file)
        rci.set_band()
        self.assertAlmostEqual(rci.get_val(point1), 0.0, delta=0.01)
        self.assertEqual(rci.get_val(point2), 1.0)
        self.assertEqual(rci.get_val(point3), 1.0)
        self.assertAlmostEqual(rci.get_val(point4), 0.5, delta=0.01)

    def test_simple_distance_nan(self):
        """ Very simple test with a raster object like thus:
             1  2  3  4
             5  6  7  8
             9  NAN NAN 12
             13 14 15 16
            (on a 20x20 grid, not 4x4 as above...only so much space
            in comments!). The slightly-left-of-centre has been
            replaced by NaN

            LLC is 0,0 and upper right is 4,4. (hence dx is 0.25)
            The data are stored in cell centres and we ask for a few coords.
            We check that the value is 1 at the distance, 0 at the boundary
            and, for this test, the value is 0 in the centre.

            The NaNs are in the centre, so the buffer is expanded by one pixel
            automatically to prevent interpolation issues
            """
        rbuff = CreateBuffer(test_file_name2, 0.5)
        point1 = [0.2, 3.85]  # should return ~0
        point2 = [0.8, 2]  # should be 0.2
        point3 = [1.7, 2]  # should be 0 (in the centre)
        rbuff.make_buffer(temp_file)
        # we now read in the buffer using the rasterinterpolator class
        rci = RasterInterpolator(temp_file)
        rci.set_band()
        self.assertAlmostEqual(rci.get_val(point1), 0.0, delta=0.03)
        self.assertAlmostEqual(rci.get_val(point2), 0.2, delta=0.03)
        self.assertEqual(rci.get_val(point3), 0.0)


if __name__ == '__main__':
    unittest.main()

import unittest
from hrds.hrds import HRDS
import os

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

base_raster = "tests/base.tif"
layer1 = "tests/layer1.tif"
layer2 = "tests/layer2.tif"

class TestHRDS(unittest.TestCase):
    """Tests the hrds.hrds.HRDS class"""
    def setUp(self):
        return

    def tearDown(self):
        # remove buffer files created
        os.remove("tests/layer1_buffer.tif")
        os.remove("tests/layer2_buffer.tif")
        return
    
    def test_simple_rasters(self):
        """ Three layer test. Base layer is 100x100 with dx of (2.5,2).
            Origin is at (0,0)
            Layer 1 is 50x75, dx of (0.5,0.5), origin at (10,10)
            Layer 2 is 25x25, dx of (0.1,0.1), origin at (30,35)
            We set a distance buffer of 7 in layer 1 and 5 in layer 2
            BaseLayer has a value of 1, layer 1 of 2 and layer 2 of three.
            We ask for points around all layers and in the buffer and check against
            those expected.
        """
        bathy = HRDS(base_raster, rasters=(layer1, layer2), distances=(7, 5))
        bathy.set_bands()
        points = ([5,5], # 1
                  [40,50], # 3
                  [28,32], # 2
                  [13.85, 20], # 1.5
                  [32.75, 45], # 2.5
                  )
        expected = [1.0, 3.0, 2.0, 1.5, 2.5]
        self.assertEqual(bathy.get_val(points[4]), expected[4])
        for p,e in zip(points, expected):
            self.assertEqual(bathy.get_val(p),e)

if __name__ == '__main__':
    unittest.main()

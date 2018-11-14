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

#@unittest.skip("Skipping this by default. 
#                Uses proprietary data.")
class RealDataTest(unittest.TestCase):

    def test_real_world(self):
        """ Mix of GEBCO, EMODnet and Marine Digimap just off the
        Norfolk/Suffolk coast.
        Projected to UTM 30, so everything in m.
        """
        bathy = HRDS("tests/real_data/gebco_uk.tif", 
                     rasters=("tests/real_data/emod_utm.tif", 
                              "tests/real_data/marine_digimap.tif"), 
                     distances=(10000, 5000))
        bathy.set_bands()
        """
        Our data:
        X          Y      emod_utm  gebco_uk  marine_dig   ID
        823862.	5782011.           -21.21704                1
        839323.	5782408.  -25.4705 -24.032                  2
        853000.	5782804.  -43.1108 -38.03058                3
        858947.	5782606.  -50.5894 -46.71868   -52.03551    4
        866083.	5783201.  -43.4241 -40.0147    -48.12579    5
        889870.	5784787.  -41.1196 -32.12536                6
        949138.	5782408.           -22.1890                 7
"""
        points = ([823862., 5782011.],
                  [839323., 5782408.],
                  #[858947., 5782606.],
                  [866083., 5783201.],
                  #[889870., 5784787.],
                  [949138., 5782408.],
                  )
        expected = [-21.21704,
                    -24.0, # estimate
                    #-43.1108,
                    -49.0, # estimate
                    -48.12579,
                    #-41.1196,
                    -22.189]
        #self.assertEqual(bathy.get_val(points[2]), expected[2])
        for p,e in zip(points, expected):
            self.assertAlmostEqual(bathy.get_val(p),e,delta=2)

    

if __name__ == '__main__':
    unittest.main()

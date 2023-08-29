import unittest
import os
import sys
# make sure we use the devel version first
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__))+'/..')
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

# this is a bit kludgy, but should work on all platforms and test frameworks

test_dir = os.path.split(__file__)[0]

base_raster = os.path.join(test_dir, "base.tif")
layer1 = os.path.join(test_dir, "layer1.tif")
layer2 = os.path.join(test_dir, "layer2.tif")


class TestHRDS(unittest.TestCase):
    """Tests the hrds.hrds.HRDS class"""

    def test_single_raster(self):
        """ A simple single raster solution"""
        
        bathy = HRDS(base_raster)
        bathy.set_bands()

        expected = [1.0,1.0,1.0,1.0,1.0] # uniform raster
        points = ([5, 5],
                  [40, 50],
                  [28, 32],
                  [13.5, 20],
                  [32.5, 45],
                  )
        for p, e in zip(points, expected):
            self.assertAlmostEqual(bathy.get_val(p), e, delta=0.1)



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

        bathy = HRDS(base_raster, rasters=(layer1, layer2), distances=(7, 5), saveBuffers=True)
        bathy.set_bands()
        points = ([5, 5],  # 1
                  [40, 50],  # 3
                  [28, 32],  # 2
                  [13.5, 20],  # 1.5
                  [32.5, 45],  # 2.5
                  )
        expected = [1.0, 3.0, 2.0, 1.5, 2.5]
        for p, e in zip(points, expected):
            self.assertAlmostEqual(bathy.get_val(p), e, delta=0.1)
        # check that the buffer files exists
        self.assertTrue(os.path.exists(os.path.join(test_dir, "layer1_buffer.tif")))
        self.assertTrue(os.path.exists(os.path.join(test_dir, "layer2_buffer.tif")))
        # delete them
        os.remove(os.path.join(test_dir, "layer1_buffer.tif"))
        os.remove(os.path.join(test_dir, "layer2_buffer.tif"))


class RealDataTest(unittest.TestCase):

    def test_real_world(self):
        """ Mix of GEBCO, EMODnet and UK Gov just off the
        Norfolk coast.
        Projected to UTM 30, so everything in m.
        """
        bathy = HRDS(os.path.join(test_dir,"real_data/gebco_uk.tif"),
                     rasters=(os.path.join(test_dir,"real_data/emod_utm.tif"),
                              os.path.join(test_dir,"real_data/inspire_data.tif")),
                     distances=(700, 200))
        bathy.set_bands()
        """
        Our data:
        X	Y	emod_utm  gebco_uk  inspire_da
        842996.	5848009.     	  -21.318
        834009.	5848207.	  -25.289
        832856.	5848273. -32.76	  -28.598
        828840.	5848306. -5.884	  -13.466
        823178.	5848503. -18.13	  -13.215
        822941.	5848511. -17.56	  -11.241  -14.554
        822762.	5848285. -5.517	  -11.241
        822634.	5848528. -6.757	  -11.241  -8.316
        822447.	5848684. -9.098	  -11.241  -10.60

"""
        points = ([842996., 5848009.],
                  [834009., 5848207.],
                  [832856., 5848273.],
                  [828840., 5848306.],
                  [823178., 5848503.],
                  [822941., 5848511.],
                  [822762., 5848285.],
                  [822634., 5848528.],
                  [822447., 5848684.],
                  )
        expected = [-21.318, #
                    -25.289,
                    -28.6,  # in the buffer, so mostly gebco
                    -5.884,
                    -18.13,
                    -17.0,  # in hi-res area, but mostly emod
                    -5.517,
                    -8.316,  # hi res are only
                    -10.60,  # as above
                    ]
        for p, e in zip(points, expected):
            self.assertAlmostEqual(bathy.get_val(p), e, delta=0.75)


class RealDataTest_limited(unittest.TestCase):

    def test_real_world_limit(self):
        """ Mix of GEBCO, EMODnet and UK Gov data just off the
        Norfolk coast.
        Projected to UTM 30, so everything in m.
        """
        bathy = HRDS(os.path.join(test_dir,"real_data/gebco_uk.tif"),
                     rasters=(os.path.join(test_dir,"real_data/emod_utm.tif"),
                              os.path.join(test_dir,"real_data/inspire_data.tif")),
                     distances=(700, 200),
                     minmax=[[None,-25],[None,-10],[None,None]])
        bathy.set_bands()
        """
        Our data:
        X	Y	emod_utm  gebco_uk  inspire_da
        842996.	5848009.     	  -21.318
        834009.	5848207.	  -25.289
        832856.	5848273. -32.76	  -28.598
        828840.	5848306. -5.884	  -13.466
        823178.	5848503. -18.13	  -13.215
        822941.	5848511. -17.56	  -11.241  -14.554
        822762.	5848285. -5.517	  -11.241
        822634.	5848528. -6.757	  -11.241  -8.316
        822447.	5848684. -9.098	  -11.241  -10.60

"""
        points = ([842996., 5848009.],
                  [834009., 5848207.],
                  [832856., 5848273.],
                  [828840., 5848306.],
                  [823178., 5848503.],
                  [822941., 5848511.],
                  [822762., 5848285.],
                  [822634., 5848528.],
                  [822447., 5848684.],
                  )
        expected = [-25.0,  # -21.318 - limited!
                    -25.289,
                    -28.6,  # in the buffer, so mostly gebco
                    -10,  # -5.884 so limited!
                    -18.13,
                    -17.0,  # in hi-res area, but mostly emod
                    -10,  # 5.517, limited
                    -8.316,  # hi res are only
                    -10.60,  # as above
                    ]
        for p, e in zip(points, expected):
            self.assertAlmostEqual(bathy.get_val(p), e, delta=0.75)


if __name__ == '__main__':
    unittest.main()

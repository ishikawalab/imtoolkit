# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
import numpy as np
from imtoolkit.Util import testUnitaryCode, getMinimumEuclideanDistance, getEuclideanDistances
from imtoolkit.ADSMCode import ADSMCode

class ADSMCodeTest(unittest.TestCase):

    def test_M2(self):
        np.set_printoptions(linewidth=np.inf)
        for L in [2, 4, 8]:
            testUnitaryCode(2, ADSMCode(2, "PSK", L))

        mind = getMinimumEuclideanDistance(ADSMCode(2, "PSK", 2).codes)
        self.assertAlmostEqual(mind, 4.0)
        mind = getMinimumEuclideanDistance(ADSMCode(2, "PSK", 2, 2.0 * np.pi / 4.0).codes)
        self.assertAlmostEqual(mind, 2.0)

    def test_M4(self):
        for L in [4, 8, 16]:
            testUnitaryCode(4, ADSMCode(4, "PSK", L))
        
if __name__ == '__main__':
    unittest.main()


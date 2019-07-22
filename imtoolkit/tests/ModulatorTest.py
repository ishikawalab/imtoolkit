# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
import numpy as np
from imtoolkit.Util import getMinimumEuclideanDistance
from imtoolkit.Modulator import Modulator

class ModulatorTest(unittest.TestCase):
    def test_PSK(self):
        for L in 2 ** np.arange(1, 8, 1):
            mod = Modulator("PSK", L)
            meanNorm = np.mean(np.power(np.abs(mod.symbols), 2))
            self.assertAlmostEqual(meanNorm, 1.0, msg = "The mean power of PSK(" + str(L) + ") symbols differs from 1.0")
            
            med = getMinimumEuclideanDistance(mod.symbols)
            self.assertGreater(med, 0, msg = "The minimum Euclidean distance of PSK(" + str(L) + ") symbols is too small")

    def test_QAM(self):
        for L in 2 ** np.arange(2, 8, 2):
            mod = Modulator("QAM", L)
            meanNorm = np.mean(np.power(np.abs(mod.symbols), 2))
            self.assertAlmostEqual(meanNorm, 1.0, msg = "The mean power of QAM(" + str(L) + ") symbols differs from 1.0")
            
            med = getMinimumEuclideanDistance(mod.symbols)
            self.assertGreater(med, 0, msg = "The minimum Euclidean distance of QAM(" + str(L) + ") symbols is too small")

    def test_StarQAM(self):
        for L in 2 ** np.arange(1, 8, 1):
            mod = Modulator("StarQAM", L)
            meanNorm = np.mean(np.power(np.abs(mod.symbols), 2))
            self.assertAlmostEqual(meanNorm, 1.0, msg = "The mean power of StarQAM(" + str(L) + ") symbols differs from 1.0")
            
            med = getMinimumEuclideanDistance(mod.symbols)
            self.assertGreater(med, 0, msg = "The minimum Euclidean distance of StarQAM(" + str(L) + ") symbols is too small")

if __name__ == '__main__':
    unittest.main()

# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
import numpy as np
from imtoolkit.Basis import Basis

class BasisTest(unittest.TestCase):
    def getMeanNorm(self, b):
        return np.mean(np.power(np.linalg.norm(b, axis=(1,2)), 2))
    
    def test_IdentityBasis(self):
        np.set_printoptions(linewidth=np.inf)
        self.assertAlmostEqual(self.getMeanNorm(Basis("i", 4, 2).bases), 2)
        self.assertAlmostEqual(self.getMeanNorm(Basis("d", 4, 2).bases), 2)
        self.assertAlmostEqual(self.getMeanNorm(Basis("r", 4, 2).bases), 2)
        self.assertAlmostEqual(self.getMeanNorm(Basis("h2", 4, 1).bases), 1)
        self.assertAlmostEqual(self.getMeanNorm(Basis("h4", 8, 2).bases), 2)

if __name__ == '__main__':
    unittest.main()

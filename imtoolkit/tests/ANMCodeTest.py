# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
import numpy as np
from imtoolkit.ANMCode import ANMCode


class ANMCodeTest(unittest.TestCase):

    def test_all(self):
        np.set_printoptions(linewidth=np.inf)

        codes = ANMCode(2, "PSK", 2).codes
        np.testing.assert_almost_equal(codes, np.array([[[1.],[0.]],[[-1.],[0.]],[[0.70710678],[0.70710678]],[[-0.70710678],[-0.70710678]]]))

        for M in [2, 4, 8]:
            for L in [2, 4, 8]:
                codes = ANMCode(M, "PSK", L).codes
                self.assertAlmostEqual(np.mean(codes), 0.0)
                self.assertAlmostEqual(np.mean(np.sum(np.square(np.abs(codes)), axis=1)), 1.0)

            for L in [4, 16, 64]:
                codes = ANMCode(M, "QAM", L).codes
                self.assertAlmostEqual(np.mean(codes), 0.0)
                self.assertAlmostEqual(np.mean(np.sum(np.square(np.abs(codes)), axis=1)), 1.0)


if __name__ == '__main__':
    unittest.main()


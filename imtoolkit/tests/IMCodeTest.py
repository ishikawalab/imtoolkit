# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
import numpy as np
from scipy.special import binom
from imtoolkit.Util import testUnitary
from imtoolkit.IMCode import IMCode


class IMCodeTest(unittest.TestCase):

    def test_M2(self):
        np.set_printoptions(linewidth=np.inf)

        codes = IMCode("opt", 2, 1, 2, "PSK", 1, 1).codes
        np.testing.assert_almost_equal(codes, np.array([[[1.],[0.]],[[0.],[1.]]]))
        codes = IMCode("dic", 4, 1, 4, "PSK", 1, 1).codes
        np.testing.assert_almost_equal(codes, np.array([[[1.],[0.],[0.],[0.]],[[0.],[1.],[0.],[0.]],[[0.],[0.],[1.],[0.]],[[0.],[0.],[0.],[1.]]]))
        codes = IMCode("wen", 4, 2, 4, "PSK", 1, 1).codes
        np.testing.assert_almost_equal(codes, np.array([[[0.70710678],[0.70710678],[0.],[0.]],[[0.],[0.70710678],[0.70710678],[0.]],[[0.],[0.],[0.70710678],[0.70710678]],[[0.70710678],[0.],[0.],[0.70710678]]]))

if __name__ == '__main__':
    unittest.main()


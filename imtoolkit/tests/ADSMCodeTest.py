# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
import numpy as np
from imtoolkit.Util import testUnitary
from imtoolkit.ADSMCode import *

class ADSMCodeTest(unittest.TestCase):

    def test_M2(self):
        np.set_printoptions(linewidth=np.inf)
        for L in [2, 4, 8]:
            testUnitary(2, ADSMCode(2, "PSK", L))

    def test_M4(self):
        for L in [4, 8, 16]:
            testUnitary(4, ADSMCode(4, "PSK", L))
        
if __name__ == '__main__':
    unittest.main()


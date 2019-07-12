# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
import numpy as np
from imtoolkit.Util import testUnitary
from imtoolkit.OSTBCode import *

class OSTBCodeTest(unittest.TestCase):

    def test_M2(self):
        for L in [2, 4, 8, 16]:
            testUnitary(2, OSTBCode(2, "PSK", L))

    def test_M4(self):
        for L in [2, 4, 8, 16]:
            testUnitary(4, OSTBCode(4, "PSK", L, nsymbols = 2))
            testUnitary(4, OSTBCode(4, "PSK", L, nsymbols = 3))
    
    def test_M16(self):
        testUnitary(16, OSTBCode(16, "PSK", 2))
        
if __name__ == '__main__':
    unittest.main()



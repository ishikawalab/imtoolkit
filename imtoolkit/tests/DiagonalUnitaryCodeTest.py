# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
import numpy as np
from imtoolkit.Util import testUnitaryCode
from imtoolkit.DiagonalUnitaryCode import DiagonalUnitaryCode

class OSTBCodeTest(unittest.TestCase):

    def test_M2(self):
        for L in [2, 4, 16, 256]:
            testUnitaryCode(2, DiagonalUnitaryCode(2, L))

    def test_M4(self):
        for L in [4, 16, 256]:
            testUnitaryCode(4, DiagonalUnitaryCode(4, L))
        
if __name__ == '__main__':
    unittest.main()



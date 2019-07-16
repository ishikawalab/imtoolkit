# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
import numpy as np
from imtoolkit.Util import testUnitary
from imtoolkit.TASTCode import *

class TASTCodeTest(unittest.TestCase):

    def test_M2(self):
        testUnitary(2, TASTCode(2, 1, 2))
        testUnitary(2, TASTCode(2, 2, 2))
        testUnitary(2, TASTCode(2, 4, 2))
        testUnitary(2, TASTCode(2, 2, 16))

    def test_M4(self):
        testUnitary(4, TASTCode(4, 1, 2))
        testUnitary(4, TASTCode(4, 2, 2))
        testUnitary(4, TASTCode(4, 2, 4))
        
if __name__ == '__main__':
    unittest.main()



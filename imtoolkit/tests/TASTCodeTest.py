# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
import numpy as np
from imtoolkit.Util import testUnitary, getMinimumEuclideanDistance
from imtoolkit.TASTCode import TASTCode

class TASTCodeTest(unittest.TestCase):

    def test_M2(self):
        c = TASTCode(2, 1, 2)
        self.assertGreater(getMinimumEuclideanDistance(c.codes), 0.0)
        testUnitary(2, c)

        c = TASTCode(2, 2, 2)
        self.assertGreater(getMinimumEuclideanDistance(c.codes), 0.0)
        testUnitary(2, c)

        c = TASTCode(2, 4, 2)
        self.assertGreater(getMinimumEuclideanDistance(c.codes), 0.0)
        testUnitary(2, c)

        c = TASTCode(2, 2, 16)
        self.assertGreater(getMinimumEuclideanDistance(c.codes), 0.0)
        testUnitary(2, c)

    def test_M4(self):
        c = TASTCode(4, 1, 2)
        self.assertGreater(getMinimumEuclideanDistance(c.codes), 0.0)
        testUnitary(4, c)

        c = TASTCode(4, 2, 2)
        self.assertGreater(getMinimumEuclideanDistance(c.codes), 0.0)
        testUnitary(4, c)

        c = TASTCode(4, 2, 4)
        self.assertGreater(getMinimumEuclideanDistance(c.codes), 0.0)
        testUnitary(4, c)
        
if __name__ == '__main__':
    unittest.main()



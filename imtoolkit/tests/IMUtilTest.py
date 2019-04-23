# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
import numpy as np
from imtoolkit.IMUtil import *

class IMUtilTest(unittest.TestCase):
    def test_convertIndsToVector(self):
        ret = convertIndsToVector([[0, 1], [0, 2]], M = 4)
        np.testing.assert_array_almost_equal(ret, [np.array([[1], [1], [0], [0]]), np.array([[1], [0], [1], [0]])])

    def test_convertIndsToMatrix(self):
        ret = convertIndsToMatrix([[0, 1], [0, 2]], M = 4)
        np.testing.assert_array_almost_equal(ret, [np.array([[1., 0.], [0., 1.], [0., 0.], [0., 0.]]), np.array([[1., 0.], [0., 0.], [0., 1.], [0., 0.]])])

    def test_getProbabilityOfActivation(self):
        ret = getProbabilityOfActivation([[0], [1], [2], [3]], 4)
        np.testing.assert_array_almost_equal(ret, np.ones(4) / 4)

    def test_getSumHamming(self):
        ret = getSumHamming(inds = [[0,1],[2,3],[1,2],[0,3]], M = 4)
        self.assertEqual(ret, 16)

    def test_checkConflict(self):
        self.assertFalse(checkConflict([[0, 1], [0, 2]]))
        self.assertTrue(checkConflict([[0, 1], [0, 1]]))

    def test_getDictionaryIndexesList(self):
        ret = getDictionaryIndexesList(4, 2, 4)
        self.assertTrue(ret == [[0, 1], [0, 2], [0, 3], [1, 2]])
    
    def test_wen2016EquiprobableSubcarrierActivation(self):
        ret = wen2016EquiprobableSubcarrierActivation(M = 2, K = 1)
        np.testing.assert_array_equal(ret, [[0], [1]])
        ret = wen2016EquiprobableSubcarrierActivation(M = 4, K = 1)
        np.testing.assert_array_equal(ret, [[0], [1], [2], [3]])
        ret = wen2016EquiprobableSubcarrierActivation(M = 4, K = 2)
        np.testing.assert_array_equal(ret, [[0, 1], [1, 2], [2, 3], [0, 3]])

if __name__ == '__main__':
    unittest.main()

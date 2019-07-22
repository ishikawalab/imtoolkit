# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
import numpy as np
import imtoolkit.Util as util

class UtilTest(unittest.TestCase):
    
    def test_getGrayIndixes(self):
        self.assertEqual(util.getGrayIndixes(2), [0, 1, 3, 2], "getGrayIndixes does not work")

    def test_frodiff(self):
        fro = util.frodiff(np.array([1, 1j, 0, 0]), np.array([1, 0, 1j, 0]))
        self.assertAlmostEqual(fro, 2.0, msg = "The Frobenius norm calculation is wrong")

    def test_getEuclideanDistances(self):
        meds = util.getEuclideanDistances(np.array([+1, -1, +1j, -1j]))
        np.testing.assert_almost_equal(meds, np.array([4., 2., 2., 2., 2., 4.]))

    def test_getMinimumEuclideanDistance(self):
        med = util.getMinimumEuclideanDistance(np.array([+1, -1, +1j, -1j]))
        self.assertAlmostEqual(med, 2.0, msg = "The MED of QPSK symbols differs from 2.0")

    def test_getDFTMatrix(self):
        W = util.getDFTMatrix(4)
        np.testing.assert_almost_equal(W.dot(W.conj().T), np.eye(4, dtype=np.complex), decimal=3)
        W = util.getDFTMatrix(8)
        np.testing.assert_almost_equal(W.dot(W.conj().T), np.eye(8, dtype=np.complex), decimal=3)
        W = util.getDFTMatrix(16)
        np.testing.assert_almost_equal(W.dot(W.conj().T), np.eye(16, dtype=np.complex), decimal=3)

    def test_inv_dB(self):
        self.assertAlmostEqual(util.inv_dB(0.0), 1.0, msg = "The implementation of inv_dB may be wrong.")
    
    def test_randn(self):
        ret = util.randn(int(1e5))
        meanPower = np.mean(np.power(np.abs(ret), 2))
        self.assertAlmostEqual(meanPower, 1.0, places = 2, msg = "The mean power of randn differs from 1.0")

    def test_randn_c(self):
        ret = util.randn_c(int(1e5))
        meanPower = np.mean(np.power(np.abs(ret), 2))
        self.assertAlmostEqual(meanPower, 1.0, places = 2, msg = "The mean power of randn_c differs from 1.0")

    def test_countErrorBits(self):
        self.assertEqual(util.countErrorBits(1, 2), 2)
        self.assertEqual(util.countErrorBits(1, 5), 1)

    def test_getXORtoErrorBitsArray(self):
        a = util.getXORtoErrorBitsArray(4)
        np.testing.assert_almost_equal(a, np.array([0, 1, 1, 2, 1]))
        a = util.getXORtoErrorBitsArray(16)
        np.testing.assert_almost_equal(a, np.array([0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, 1]))

    def test_getErrorBitsTable(self):
        t = util.getErrorBitsTable(4)
        np.testing.assert_almost_equal(t, np.array([[0,1,1,2],[1,0,2,1],[1,2,0,1],[2,1,1,0]]))
        t = util.getErrorBitsTable(8)
        np.testing.assert_almost_equal(t, np.array([[0,1,1,2,1,2,2,3],[1,0,2,1,2,1,3,2],[1,2,0,1,2,3,1,2],[2,1,1,0,3,2,2,1],[1,2,2,3,0,1,1,2],[2,1,3,2,1,0,2,1],[2,3,1,2,1,2,0,1],[3,2,2,1,2,1,1,0]]))

    def test_getXCorrespondingToY(self):
        a = util.getXCorrespondingToY(np.array([0,1]), np.array([0,1]), 0.5)
        np.testing.assert_almost_equal(a, np.array(0.5))

    def test_getRandomHermitianMatrix(self):
        np.set_printoptions(linewidth=np.inf)
        H = util.getRandomHermitianMatrix(4)
        np.testing.assert_almost_equal(H, H.conj().T)
        H = util.getRandomHermitianMatrix(8)
        np.testing.assert_almost_equal(H, H.conj().T)
        H = util.getRandomHermitianMatrix(16)
        np.testing.assert_almost_equal(H, H.conj().T)

    def test_CayleyTransform(self):
        U = util.CayleyTransform(util.getRandomHermitianMatrix(4))
        np.testing.assert_almost_equal(U.dot(U.conj().T), np.eye(4, dtype=np.complex))
        U = util.CayleyTransform(util.getRandomHermitianMatrix(8))
        np.testing.assert_almost_equal(U.dot(U.conj().T), np.eye(8, dtype=np.complex))
        U = util.CayleyTransform(util.getRandomHermitianMatrix(16))
        np.testing.assert_almost_equal(U.dot(U.conj().T), np.eye(16, dtype=np.complex))

if __name__ == '__main__':
    unittest.main()

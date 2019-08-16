# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt
import unittest
import os
import numpy as np
if os.getenv("USECUPY") == "1":
    import cupy as xp
else:
    import numpy as xp
import imtoolkit.Util as util
from imtoolkit import Modulator, IMCode, DiagonalUnitaryCode

class UtilTest(unittest.TestCase):
    
    def test_getGrayIndixes(self):
        self.assertEqual(util.getGrayIndixes(2), [0, 1, 3, 2])
        self.assertEqual(util.getGrayIndixes(4), [0, 1, 3, 2, 6, 7, 5, 4, 12, 13, 15, 14, 10, 11, 9, 8])

    def test_frodiff(self):
        fro = util.frodiff(xp.array([1, 1j, 0, 0]), xp.array([1, 0, 1j, 0]))
        self.assertAlmostEqual(fro, 2.0, msg = "The Frobenius norm calculation is wrong")
        fro = util.frodiff(util.randn_c(int(1e6)), util.randn_c(int(1e6)))
        self.assertAlmostEqual(fro/2e6, 1.0, places = 2)

    def test_getEuclideanDistances(self):
        codes = Modulator("PSK", 4).symbols.reshape(4, 1, 1)
        ret = util.asnumpy(util.getEuclideanDistances(xp.array(codes)))
        np.testing.assert_almost_equal(ret, [2., 2., 4., 4., 2., 2.])
        #
        codes = IMCode("opt", 2, 1, 2, "PSK", 1, 1).codes
        ret = util.asnumpy(util.getEuclideanDistances(xp.array(codes)))
        np.testing.assert_almost_equal(ret, [2.])
        #
        codes = IMCode("opt", 4, 2, 4, "PSK", 1, 1).codes
        ret = util.asnumpy(util.getEuclideanDistances(xp.array(codes)))
        np.testing.assert_almost_equal(ret, [1., 1., 2., 2., 1., 1.])
        #
        codes = DiagonalUnitaryCode(2, 2).codes
        ret = util.asnumpy(util.getEuclideanDistances(xp.array(codes)))
        np.testing.assert_almost_equal(ret, [16.])

    def test_getMinimumEuclideanDistance(self):
        codes = Modulator("PSK", 4).symbols.reshape(4, 1, 1)
        med = util.getMinimumEuclideanDistance(xp.array(codes))
        self.assertAlmostEqual(med, 2.0)

        codes = Modulator("SQAM", 16).symbols.reshape(16, 1, 1)
        med = util.getMinimumEuclideanDistance(xp.array(codes))
        self.assertAlmostEqual(med, 0.2343145750507619)
        
        codes = IMCode("opt", 4, 2, 4, "PSK", 4, 1).codes
        med = util.getMinimumEuclideanDistance(xp.array(codes))
        self.assertAlmostEqual(med, 1.0)

    def test_getDFTMatrix(self):
        W = util.getDFTMatrix(4)
        xp.testing.assert_almost_equal(W.dot(W.conj().T), xp.eye(4, dtype=xp.complex), decimal=3)
        W = util.getDFTMatrix(8)
        xp.testing.assert_almost_equal(W.dot(W.conj().T), xp.eye(8, dtype=xp.complex), decimal=3)
        W = util.getDFTMatrix(16)
        xp.testing.assert_almost_equal(W.dot(W.conj().T), xp.eye(16, dtype=xp.complex), decimal=3)

    def test_inv_dB(self):
        self.assertAlmostEqual(util.inv_dB(0.0), 1.0, msg = "The implementation of inv_dB may be wrong.")
    
    def test_randn(self):
        ret = util.randn(int(1e6))
        meanPower = xp.mean(xp.power(xp.abs(ret), 2))
        self.assertAlmostEqual(meanPower, 1.0, places = 2, msg = "The mean power of randn differs from 1.0")

    def test_randn_c(self):
        ret = util.randn_c(int(1e6))
        meanPower = xp.mean(xp.power(xp.abs(ret), 2))
        self.assertAlmostEqual(meanPower, 1.0, places = 2, msg = "The mean power of randn_c differs from 1.0")

    def test_countErrorBits(self):
        self.assertEqual(util.countErrorBits(1, 2), 2)
        self.assertEqual(util.countErrorBits(1, 5), 1)

    def test_getXORtoErrorBitsArray(self):
        a = util.getXORtoErrorBitsArray(4)
        xp.testing.assert_almost_equal(a, xp.array([0, 1, 1, 2, 1]))
        a = util.getXORtoErrorBitsArray(16)
        xp.testing.assert_almost_equal(a, xp.array([0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, 1]))

    def test_getErrorBitsTable(self):
        t = util.getErrorBitsTable(4)
        xp.testing.assert_almost_equal(t, xp.array([[0,1,1,2],[1,0,2,1],[1,2,0,1],[2,1,1,0]]))
        t = util.getErrorBitsTable(8)
        xp.testing.assert_almost_equal(t, xp.array([[0,1,1,2,1,2,2,3],[1,0,2,1,2,1,3,2],[1,2,0,1,2,3,1,2],[2,1,1,0,3,2,2,1],[1,2,2,3,0,1,1,2],[2,1,3,2,1,0,2,1],[2,3,1,2,1,2,0,1],[3,2,2,1,2,1,1,0]]))

    def test_getXCorrespondingToY(self):
        a = util.getXCorrespondingToY(xp.array([0,1]), xp.array([0,1]), 0.5)
        xp.testing.assert_almost_equal(a, xp.array(0.5))

    def test_getRandomHermitianMatrix(self):
        xp.set_printoptions(linewidth=xp.inf)
        H = util.getRandomHermitianMatrix(4)
        xp.testing.assert_almost_equal(H, H.conj().T)
        H = util.getRandomHermitianMatrix(8)
        xp.testing.assert_almost_equal(H, H.conj().T)
        H = util.getRandomHermitianMatrix(16)
        xp.testing.assert_almost_equal(H, H.conj().T)

    def test_CayleyTransform(self):
        U = util.CayleyTransform(util.getRandomHermitianMatrix(4))
        xp.testing.assert_almost_equal(U.dot(U.conj().T), xp.eye(4, dtype=xp.complex))
        U = util.CayleyTransform(util.getRandomHermitianMatrix(8))
        xp.testing.assert_almost_equal(U.dot(U.conj().T), xp.eye(8, dtype=xp.complex))
        U = util.CayleyTransform(util.getRandomHermitianMatrix(16))
        xp.testing.assert_almost_equal(U.dot(U.conj().T), xp.eye(16, dtype=xp.complex))

if __name__ == '__main__':
    unittest.main()

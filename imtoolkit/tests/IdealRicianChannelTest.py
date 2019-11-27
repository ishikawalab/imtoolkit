# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
import numpy as np
from imtoolkit.Util import frequencyToWavelength
from imtoolkit.IdealRicianChannel import IdealRicianChannel

class IdealRicianChannelTest(unittest.TestCase):

    def test_ChannelM2ULA(self):
        np.set_printoptions(linewidth=np.inf)
        wavelength = frequencyToWavelength(5.0 * 10 ** 9) # 5 [GHz]
        IT, M, N, ae_spacing, distance_tx_rx = 10000, 2, 2, wavelength / 2, 5.0
        tx, ty, tz = IdealRicianChannel.getPositionsUniformLinearArray(M, ae_spacing, 0)
        rx, ry, rz = IdealRicianChannel.getPositionsUniformLinearArray(N, ae_spacing, distance_tx_rx)
        channel = IdealRicianChannel(IT, 10, wavelength, tx, ty, tz, rx, ry, rz)
        channel.randomize()
        H = channel.getChannel().reshape(IT, N, M)
        norms = np.square(np.linalg.norm(H, axis=(1, 2)))
        self.assertAlmostEqual(np.mean(norms), M * N, places=1)

        meanrank = np.mean(np.linalg.matrix_rank(H))
        self.assertAlmostEqual(meanrank, M)

    def test_ChannelM4ULA(self):
        np.set_printoptions(linewidth=np.inf)
        wavelength = frequencyToWavelength(5.0 * 10 ** 9)  # 5 [GHz]
        IT, M, N, ae_spacing, distance_tx_rx = 100000, 4, 4, wavelength / 2, 5.0
        tx, ty, tz = IdealRicianChannel.getPositionsUniformLinearArray(M, ae_spacing, 0)
        rx, ry, rz = IdealRicianChannel.getPositionsUniformLinearArray(N, ae_spacing, distance_tx_rx)
        channel = IdealRicianChannel(IT, 2.5, wavelength, tx, ty, tz, rx, ry, rz)
        channel.randomize()
        H = channel.getChannel().reshape(IT, N, M)
        norms = np.square(np.linalg.norm(H, axis=(1, 2)))
        self.assertAlmostEqual(np.mean(norms), M * N, places=1)

        meanrank = np.mean(np.linalg.matrix_rank(H))
        self.assertAlmostEqual(meanrank, M)

        print(np.mean(np.linalg.svd(H)[1], axis=0))

    def test_ChannelM16ULA(self):
        np.set_printoptions(linewidth=np.inf)
        wavelength = frequencyToWavelength(5.0 * 10 ** 9)  # 5 [GHz]
        IT, M, N, ae_spacing, distance_tx_rx = 100000, 16, 4, wavelength / 2, 5.0
        tx, ty, tz = IdealRicianChannel.getPositionsUniformLinearArray(M, ae_spacing, 0)
        rx, ry, rz = IdealRicianChannel.getPositionsUniformLinearArray(N, ae_spacing, distance_tx_rx)
        channel = IdealRicianChannel(IT, 2.5, wavelength, tx, ty, tz, rx, ry, rz)
        channel.randomize()
        H = channel.getChannel().reshape(IT, N, M)
        norms = np.square(np.linalg.norm(H, axis=(1, 2)))
        self.assertAlmostEqual(np.mean(norms), M * N, places=1)

        meanrank = np.mean(np.linalg.matrix_rank(H))
        self.assertAlmostEqual(meanrank, N)

        print(np.mean(np.linalg.svd(H)[1], axis=0))

    def test_ChannelM16ULAbohagen(self):
        np.set_printoptions(linewidth=np.inf)
        wavelength = frequencyToWavelength(5.0 * 10 ** 9)  # 5 [GHz]
        IT, M, N, ae_spacing, distance_tx_rx = 100000, 16, 4, wavelength, 5.0
        rx, ry, rz = IdealRicianChannel.getPositionsUniformLinearArray(N, ae_spacing, distance_tx_rx)
        dtx = distance_tx_rx / max(M, N)
        tx, ty, tz = IdealRicianChannel.getPositionsUniformLinearArray(M, dtx, 0)
        channel = IdealRicianChannel(IT, 2.5, wavelength, tx, ty, tz, rx, ry, rz)
        channel.randomize()
        H = channel.getChannel().reshape(IT, N, M)
        norms = np.square(np.linalg.norm(H, axis=(1, 2)))
        self.assertAlmostEqual(np.mean(norms), M * N, places=1)

        meanrank = np.mean(np.linalg.matrix_rank(H))
        self.assertAlmostEqual(meanrank, N)

        print(np.mean(np.linalg.svd(H)[1], axis=0))

    def test_ChannelM16N4Rec(self):
        np.set_printoptions(linewidth=np.inf)
        wavelength = frequencyToWavelength(5.0 * 10 ** 9)  # 5 [GHz]
        IT, M, N = 100000, 16, 4
        tx, ty, tz = IdealRicianChannel.getPositionsRectangular2d(M, wavelength, 3.0)
        rx, ry, rz = IdealRicianChannel.getPositionsRectangular2d(N, wavelength, 0.0)

        channel = IdealRicianChannel(IT, 2.5, wavelength, tx, ty, tz, rx, ry, rz)
        channel.randomize()
        H = channel.getChannel().reshape(IT, N, M)
        norms = np.square(np.linalg.norm(H, axis=(1, 2)))
        self.assertAlmostEqual(np.mean(norms), M * N, places=1)

        meanrank = np.mean(np.linalg.matrix_rank(H))
        self.assertAlmostEqual(meanrank, N)

        print(np.mean(np.linalg.svd(H)[1], axis=0))

    def test_ChannelM16N8Rec(self):
        np.set_printoptions(linewidth=np.inf)
        wavelength = frequencyToWavelength(5.0 * 10 ** 9)  # 5 [GHz]
        IT, M, N = 100000, 16, 8
        tx, ty, tz = IdealRicianChannel.getPositionsRectangular2d(M, wavelength, 3.0)
        rx, ry, rz = IdealRicianChannel.getPositionsRectangular2d(N, wavelength, 0.0)

        channel = IdealRicianChannel(IT, 2.5, wavelength, tx, ty, tz, rx, ry, rz)
        channel.randomize()
        H = channel.getChannel().reshape(IT, N, M)
        norms = np.square(np.linalg.norm(H, axis=(1, 2)))
        self.assertAlmostEqual(np.mean(norms), M * N, places=1)

        meanrank = np.mean(np.linalg.matrix_rank(H))
        self.assertAlmostEqual(meanrank, N)

        print(np.mean(np.linalg.svd(H)[1], axis=0))

if __name__ == '__main__':
    unittest.main()

# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
import numpy as np
from imtoolkit.Util import frequencyToWavelength
from imtoolkit.IdealRicianChannel import IdealRicianChannel

class IdealRicianChannelTest(unittest.TestCase):

    def test_ChannelM2(self):
        np.set_printoptions(linewidth=np.inf)
        wavelength = frequencyToWavelength(5.0 * 10 ** 9) # 5 [GHz]
        IT, M, N, ae_spacing, distance_tx_rx = 10000, 2, 2, wavelength / 2, 5.0
        tx, ty, rx, ry = IdealRicianChannel.getPositionsSingleArray(M, N, ae_spacing, distance_tx_rx)
        channel = IdealRicianChannel(IT, 10, wavelength, tx, ty, rx, ry)
        channel.randomize()
        H = channel.getChannel().reshape(IT, N, M)
        norms = np.square(np.linalg.norm(H, axis=(1, 2)))
        self.assertAlmostEqual(np.mean(norms), M * N, places=1)

        meanrank = np.mean(np.linalg.matrix_rank(H))
        self.assertAlmostEqual(meanrank, M)

    def test_ChannelM4(self):
        np.set_printoptions(linewidth=np.inf)
        wavelength = frequencyToWavelength(5.0 * 10 ** 9)  # 5 [GHz]
        IT, M, N, ae_spacing, distance_tx_rx = 100000, 4, 4, wavelength / 2, 5.0
        tx, ty, rx, ry = IdealRicianChannel.getPositionsSingleArray(M, N, ae_spacing, distance_tx_rx)
        channel = IdealRicianChannel(IT, 2.5, wavelength, tx, ty, rx, ry)
        channel.randomize()
        H = channel.getChannel().reshape(IT, N, M)
        norms = np.square(np.linalg.norm(H, axis=(1, 2)))
        self.assertAlmostEqual(np.mean(norms), M * N, places=1)

        meanrank = np.mean(np.linalg.matrix_rank(H))
        self.assertAlmostEqual(meanrank, M)

        print(np.mean(np.linalg.svd(H)[1], axis=0))


if __name__ == '__main__':
    unittest.main()

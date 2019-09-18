# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import os
if os.getenv("USECUPY") == "1":
    import cupy as xp
else:
    import numpy as xp
from .Channel import Channel
from .Util import randn_c


class IdealRicianChannel(Channel):
    """
    A `Channel` class that generates the ideal Rician (or Ricean) fading channel coefficients. The basic model of this implementation is based on [1].

    [1] F. Bøhagen, P. Orten, and G. E. Øien, ``Design of optimal high-rank line-of-sight MIMO channels,'' IEEE Trans. Wirel. Commun., vol. 6, no. 4, pp. 1420--1424, 2007.
    """
    def __init__(self, IT, K_dB, wavelength, tx, ty, rx, ry):
        """
        Args:
            IT (int): the number of parallel channel matrices.
            K_dB (float): the rician K factor in dB.
            wavelength (float): the wavelength.
            tx (numpy.array): the x positions of transmit antenna elements.
            ty (numpy.array): the x positions of transmit antenna elements.
            rx (numpy.array): the x positions of receive antenna elements.
            ry (numpy.array): the x positions of receive antenna elements.
        """
        self.IT = IT
        self.K = 10 ** (K_dB / 10.0)
        self.M = len(tx) # the number of transmit antenna elements
        self.N = len(rx) # the number of receive antenna elements

        r = xp.zeros((self.N, self.M), dtype = xp.complex)
        for n in range(self.N):
            for m in range(self.M):
                r[n][m] = xp.sqrt(xp.square(rx[n] - tx[m]) + xp.square(ry[n] - ty[m]))

        anHLoS = xp.exp(-1j * 2.0 * xp.pi / wavelength * r)
        self.HLoS = xp.tile(anHLoS.T, IT).T # IT \cdot N \times M

    def randomize(self):
        self.channelMatrix = xp.sqrt(self.K / (1.0 + self.K)) * self.HLoS + randn_c(self.IT * self.N, self.M) / xp.sqrt(self.K + 1.0)
    
    def getChannel(self):
        return self.channelMatrix

    def getEstimate(self):
        # Perfect channel state informaiton at the receiver
        return self.channelMatrix

    @classmethod
    def getPositionsSingleArray(cls, M, N, ae_spacing, distance_tx_rx):
        tx = xp.arange(M) * ae_spacing
        rx = xp.arange(N) * ae_spacing

        # centering
        tx -= (tx[0] + tx[-1]) / 2.0
        rx -= (rx[0] + rx[-1]) / 2.0

        ty = xp.array([distance_tx_rx] * M)
        ry = xp.zeros(N)

        return tx, ty, rx, ry

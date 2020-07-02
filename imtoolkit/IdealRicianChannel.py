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
    def __init__(self, IT, K_dB, wavelength, tx, ty, tz, rx, ry, rz):
        """
        Args:
            IT (int): the number of parallel channel matrices.
            K_dB (float): the rician K factor in dB.
            wavelength (float): the wavelength.
            tx (numpy.array): the x positions of transmit antenna elements.
            ty (numpy.array): the y positions of transmit antenna elements.
            tz (numpy.array): the z positions of transmit antenna elements.
            rx (numpy.array): the x positions of receive antenna elements.
            ry (numpy.array): the y positions of receive antenna elements.
            rz (numpy.array): the z positions of receive antenna elements.
        """
        self.IT = IT
        self.K = 10 ** (K_dB / 10.0)
        self.M = len(tx) # the number of transmit antenna elements
        self.N = len(rx) # the number of receive antenna elements

        r = xp.zeros((self.N, self.M), dtype = xp.complex)
        for n in range(self.N):
            for m in range(self.M):
                r[n][m] = xp.sqrt(xp.square(rx[n] - tx[m]) + xp.square(ry[n] - ty[m]) + xp.square(rz[n] - tz[m]))

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
    def getPositionsUniformLinearArray(cls, Nae, ae_spacing, height):
        x = xp.arange(Nae) * ae_spacing
        x -= xp.mean(x) # centering
        y = xp.zeros(Nae)
        z = xp.repeat(xp.array(height), Nae)

        return x, y, z

    @classmethod
    def getPositionsRectangular2d(cls, Nae, ae_spacing, height):
        sq = xp.floor(xp.sqrt(Nae))
        x = xp.arange(Nae) % sq
        y = xp.floor(xp.arange(Nae) / sq)
        z = xp.repeat(xp.array(height), Nae)

        x *= ae_spacing
        y *= ae_spacing

        x -= xp.mean(x)
        y -= xp.mean(y)

        return x, y, z
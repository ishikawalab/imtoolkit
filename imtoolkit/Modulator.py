# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import numpy as np
from .Util import getGrayIndixes


# Pahse-shift keying
class PSK(object):
    def __init__(self, constellationSize=2):
        self.constellationSize = L = constellationSize
        self.bitWidth = np.log2(L)

        if self.bitWidth != np.floor(self.bitWidth):
            print("The specified constellationSize is not a power of two")
            return

        if L == 1:
            self.symbols = [1]
            return

        grayIndexes = getGrayIndixes(self.bitWidth)
        originalSymbols = np.exp(2.0j * np.pi * np.asarray(range(L)) / L)
        # We would like to avoid quantization errors
        l4 = np.min([L, 4])
        indsAxis = (np.arange(l4) * L / l4).astype(np.int)
        originalSymbols[indsAxis] = np.rint(originalSymbols[indsAxis])
        self.symbols = np.take(originalSymbols, grayIndexes)


# Quadrature amplitude modulation
class QAM(object):
    def __init__(self, constellationSize=4):
        self.constellationSize = L = constellationSize
        self.bitWidth = np.log2(L)
        sqrtL = np.floor(np.sqrt(L))

        if sqrtL * sqrtL != L:
            print("The specified constellationSize is not an even power of two")
            return

        sigma = np.sqrt((L - 1) * 2.0 / 3.0)
        y = np.floor(np.arange(L) / sqrtL)
        x = np.arange(L) % sqrtL
        originalSymbols = ((sqrtL - 1) - 2.0 * x) / sigma + 1j * ((sqrtL - 1) - 2.0 * y) / sigma

        logsqL = np.floor(np.log2(sqrtL))
        grayIndexes = getGrayIndixes(logsqL)
        grayIndexes = (np.take(grayIndexes, list(y)) * 2 ** logsqL + np.take(grayIndexes, list(x))).astype(np.int)
        # grayIndexes

        self.symbols = np.take(originalSymbols, grayIndexes)


class StarQAM(object):
    """
    This StarQAM class is an efficient implementation of the following paper [1].

    - [1] W. T. Webb, L. Hanzo, and R. Steele, "Bandwidth efficient QAM schemes for Rayleigh fading channels," IEE Proc., vol. 138, no. 3, pp. 169--175, 1991.
    """
    def __init__(self, constellationSize=2):
        self.constellationSize = L = constellationSize
        self.bitWidth = np.log2(L)
        p = np.log2(L) / 2 - 1
        subConstellationSize = int(4 * 2 ** np.floor(p))
        Nlevels = int(2 ** np.ceil(p))

        # print("subConstellationSize * Nlevels = " + str(subConstellationSize) + " * " + str(Nlevels) + " = " + str(subConstellationSize * Nlevels))

        sigma = np.sqrt(6.0 / (Nlevels + 1.0) / (2.0 * Nlevels + 1.0))
        self.symbols = np.zeros(L, dtype=np.complex)
        for level_id in range(Nlevels):
            mod = PSK(subConstellationSize)
            # self.symbols.append((1.0 + level_id) * sigma * mod.symbols)
            self.symbols[(level_id * subConstellationSize):((level_id + 1) * subConstellationSize)] = (1.0 + level_id) * sigma * mod.symbols

        # print("StartQAM: the constellation size of " + str(L) + " is not supported yet")


class Modulator(object):
    """
    This class generates a constellation such as PSK, QAM, and star-QAM (SQAM).
    """

    def __init__(self, mode="PSK", constellationSize=2):
        """
        Args:
            mode (string): the type of constellation, such as PSK, QAM, and SQAM.
            L (int): the constellation size.
        """
        self.constellationSize = constellationSize
        self.bitWidth = np.log2(constellationSize)
        if mode == "PSK":
            self.symbols = PSK(constellationSize).symbols
        elif mode == "QAM":
            self.symbols = QAM(constellationSize).symbols
        elif mode == "SQAM" or mode == "StarQAM":
            self.symbols = StarQAM(constellationSize).symbols

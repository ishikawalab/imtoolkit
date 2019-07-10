# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import importlib
import numpy as np
from .Util import *

# Pahse-shift keying
class PSK:
    def __init__(self, constellationSize = 2):
        self.L = constellationSize
        self.bitWidth = np.log2(self.L)

        if self.bitWidth != np.floor(self.bitWidth):
            print("The specified constellationSize is not a power of two")
            return

        if self.L == 1:
            self.symbols = [1]
            return

        grayIndexes = getGrayIndixes(self.bitWidth)
        originalSymbols = np.exp(2.0j * np.pi * np.asarray(range(self.L)) / self.L)
        # We would like to avoid quantization errors
        l4 = np.min([self.L, 4])
        indsAxis = (np.arange(l4) * self.L / l4).astype(np.int)
        originalSymbols[indsAxis] = np.rint(originalSymbols[indsAxis])
        self.symbols = np.take(originalSymbols, grayIndexes)

# Quadrature amplitude modulation
class QAM:
    def __init__(self, constellationSize = 4):
        self.L = constellationSize
        self.bitWidth = np.log2(self.L)
        sqrtL = np.floor(np.sqrt(self.L))

        if sqrtL * sqrtL != self.L:
            print("The specified constellationSize is not an even power of two")
            return
      
        logsqL = np.floor(np.log2(sqrtL))
        sigma = np.sqrt((self.L - 1) * 2.0 / 3.0)
        y = np.floor(np.arange(self.L) / sqrtL)
        x = np.arange(self.L) % sqrtL
        originalSymbols = ((sqrtL - 1) - 2.0 * x) / sigma + 1j * ((sqrtL - 1) - 2.0 * y) / sigma
        #originalSymbols
        
        grayIndexes = getGrayIndixes(logsqL)
        grayIndexes = (np.take(grayIndexes, list(y)) * 2 ** logsqL + np.take(grayIndexes, list(x))).astype(np.int)
        #grayIndexes

        self.symbols = np.take(originalSymbols, grayIndexes)


# This StarQAM class is an efficient implementation of the following paper.
# W. T. Webb, L. Hanzo, and R. Steele, ``Bandwidth efficient QAM schemes for Rayleigh fading channels,'' IEE Proc., vol. 138, no. 3, pp. 169--175, 1991.
class StarQAM:
    def __init__(self, constellationSize = 2):
        self.L = constellationSize
        self.bitWidth = np.log2(self.L)
        p = np.log2(self.L) / 2 - 1
        self.subConstellationSize = int(4 * 2 ** np.floor(p))
        self.Nlevels = int(2 ** np.ceil(p))

        print("self.subConstellationSize * self.Nlevels = " + str(self.subConstellationSize) + " * " + str(self.Nlevels) + " = " + str(self.subConstellationSize * self.Nlevels))

        sigma = np.sqrt(6.0 / (self.Nlevels + 1.0) / (2.0 * self.Nlevels + 1.0))
        self.symbols = []
        for level_id in range(self.Nlevels):
            mod = PSK(self.subConstellationSize)
            self.symbols.append((1.0 + level_id) * sigma * mod.symbols)
            

        #print("StartQAM: the constellation size of " + str(self.L) + " is not supported yet")

class Modulator:
    """Generate a constellation such as PSK, QAM, and star-QAM (SQAM).

    Args:
        mode (string): the type of constellation, such as PSK, QAM, and SQAM.
        L (int): the constellation size.
    """

    def __init__(self, mode = "PSK", constellationSize = 2):
        self.constellationSize = constellationSize
        if mode == "PSK":
            self.symbols = PSK(constellationSize).symbols
        elif mode == "QAM":
            self.symbols = QAM(constellationSize).symbols
        elif mode == "SQAM" or mode == "StarQAM":
            self.symbols = StarQAM(constellationSize).symbols



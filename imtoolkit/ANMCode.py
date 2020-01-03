# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import numpy as np
from .Modulator import Modulator


class ANMCode(object):
    def __init__(self, M, modtype, L):
        mod = Modulator(modtype, L)
        self.codes = np.zeros((M * L, M, 1), dtype=np.complex)

        for m in range(M):
            for l in range(L):
                for k in range(m+1):
                    self.codes[m * L + l, k, 0] = mod.symbols[l] / np.sqrt(m+1)

        self.B1 = np.floor(np.log2(M))
        self.B2 = np.floor(np.log2(L))
        self.B = self.B1 + self.B2

    def putRate(self):
        print("B = B1 + B2 = %d + %d = %d [bit/symbol]" % (self.B1, self.B2, self.B))

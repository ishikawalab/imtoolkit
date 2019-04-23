# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import numpy as np
from scipy import special
from .Modulator import *
from .Util import *
from .IMUtil import *

class IMCode:
    def __init__(self, dm, M, K, Q, mod, L, meanPower):
        mod = Modulator(mod, L)
        kfoldsymbols = np.array(list(itertools.product(mod.symbols, repeat = K))).T
        self.inds = getIndexes(dm, M, K, Q)
        Q = len(self.inds)
        indsm = convertIndsToMatrix(self.inds, M)
        self.codes = np.matmul(indsm, kfoldsymbols / np.sqrt(K))
        self.codes *= np.sqrt(meanPower) # the mean power is normalized to meanPower
        self.codes = np.hsplit(np.hstack(self.codes), Q * kfoldsymbols.shape[1]) # Nc \times M \times 1

        self.B1 = np.floor(np.log2(Q))
        self.B2 = int(K * np.log2(L))
        self.B = self.B1 + self.B2
    
    def putRate(self):
        print("B = B1 + B2 = %d + %d = %d [bits/symbol]"%(self.B1, self.B2, self.B))
    


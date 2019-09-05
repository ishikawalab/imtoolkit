# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import numpy as np
from .Modulator import Modulator


class SymbolCode(object):
    def __init__(self, modtype, L):
        self.codes = np.array(Modulator(modtype, L).symbols).reshape(L, 1, 1)
        self.B = int(np.log2(L))

    def putRate(self):
        print("B = %d [bit/symbol]" % (self.B))

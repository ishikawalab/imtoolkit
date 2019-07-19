# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import numpy as np
import scipy
from .Util import *

class Basis:
    """This class generates a basis set for nonsquare differential encoding and decoding, which is proposed in [1,2].

    [1] N. Ishikawa, R. Rajashekar, C. Xu, S. Sugiura, and L. Hanzo, ``Differential space-time coding dispensing with channel-estimation approaches the performance of its coherent counterpart in the open-loop massive MIMO-OFDM downlink,'' IEEE Trans. Commun., vol. 66, no. 12, pp. 6190–6204, 2018.

    [2] N. Ishikawa, R. Rajashekar, C. Xu, M. El-Hajjar, S. Sugiura, L. L. Yang, and L. Hanzo, ``Differential-detection aided large-scale generalized spatial modulation is capable of operating in high-mobility millimeter-wave channels,'' IEEE J. Sel. Top. Signal Process., in press.

    Args:
        type (string): the basis type, such as i (IdentityBasis) and d (DFTBasis).
        M (int): the number of transmit antennas.
        T (int): the number of reduced time slots.
    """

    def __init__(self, type, M, T):
        self.type = type
        self.M = M
        self.T = T

        # initialize a unitary matrix that generates a set of bases
        if type[0].lower() == 'i':
            # Identity basis
            U = np.eye(M, dtype = np.complex)
        elif type[0].lower() == 'd':
            # DFT basis
            U = getDFTMatrix(M)
        elif type[0].lower() == 'r':
            # Random basis
            U = CayleyTransform(getRandomHermitianMatrix(M))
        elif type[0].lower() == 'h':
            P = int(type.replace('h',''))
            W = getDFTMatrix(P)
            U = zeros((M, M), dtype=complex)
            for i in range(int(M / P)):
                U[(i * P) : (i * P + P), (i * P) : (i * P + P)] = W
        
        self.bases = self.convertUnitaryToBases(U) # (M/T) \times M \times T

    def convertUnitaryToBases(self, U):
        return np.array(np.hsplit(U, self.M / self.T))


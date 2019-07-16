# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import itertools
from math import *
import numpy as np
from .Modulator import StarQAM
from .Util import *

class TASTCode:
    """Differential space-time shift keying using threaded algebraic space-time (DSTSK-TAST) coding, which was proposed in [1]. Other relevant papers are found in [2,3]. 

    [1] C. Xu, P. Zhang, R. Rajashekar, N. Ishikawa, S. Sugiura, L. Wang, and L. Hanzo, ``Finite-cardinality single-RF differential space-time modulation for improving the diversity-throughput tradeoff,'' IEEE Trans. Commun. Press, vol. 67, no. 1, pp. 318--335, 2019.

    [2] C. Xu, R. Rajashekar, N. Ishikawa, S. Sugiura, and L. Hanzo, ``Single-RF index shift keying aided differential space-time block coding,'' IEEE Trans. Signal Process., vol. 66, no. 3, pp. 773--788, 2018.

    [3] C. Xu, P. Zhang, R. Rajashekar, N. Ishikawa, S. Sugiura, Z. Wang, and L. Hanzo, ````Near-perfect'' finite-cardinality generalized space-time shift keying,'' IEEE J. Sel. Areas Commun., in press.

    Args:
        M (int): the number of transmit antennas.
        Q (int): the number of dispersion elements.
        L (int): the SQAM constellation size.
    """

    def __init__(self, M, Q, L):
        self.Nc = M * L * Q
        self.B = np.log2(self.Nc)

        mod = StarQAM(L)
        apsksymbols = mod.symbols
        La = mod.Nlevels
        Lp = mod.subConstellationSize

        G = np.zeros((M, M), dtype=np.complex)
        G[0, M - 1] = 1
        for m in range(M-1):
            G[m + 1, m] = 1
        
        msymbols = np.exp(1j * 2.0 * np.pi * np.arange(M) / (Lp * max(M, Q)))
        u = self.getDiversityMaximizingFactors(M, Q, La, Lp)
        
        self.codes = zeros((M * L * Q, M, M), dtype = np.complex)
        for l in range(L):
            for m in range(M):
                for q in range(Q):
                    qsymbols = np.exp(1j * 2.0 * np.pi * u * np.arange(M) / (L * Q))
                    self.codes[Q * M * l + m * Q + q] = matmul(apsksymbols[l] * msymbols[m] * linalg.matrix_power(G, m), diag(qsymbols))

    def putRate(self):
        print("B = %d [bit/symbol]" % self.B)

    def getDiversityMaximizingFactors(self, M, Q, La, Lp):
        if M == 2 and Q == 1 and La == 1 and Lp == 2:
        	# Rate = 1
        	u = [1,1]
        elif M == 2 and Q == 2 and La == 1 and Lp == 2:
        	# Rate = 1.5
        	u = [1,3]
        elif M == 2 and Q == 4 and La == 1 and Lp == 2:
        	# Rate = 2
        	u = [1,3]
        elif M == 2 and Q == 2 and La == 1 and Lp == 8:
        	# Rate = 2.5
        	#u = [1,7] [1, p. 22]
        	#u = [3,13] [1, p. 26]
        	u = [15,5]
        elif M == 2 and Q == 2 and La == 2 and Lp == 8:
        	# Rate = 3
        	#u = [3,13] # [1, p. 22]
        	u = [2,14]
        elif M == 2 and Q == 4 and La == 1 and Lp == 8:
        	# Rate = 3
        	u = [1,7]
        elif M == 2 and Q == 4 and La == 2 and Lp == 8:
        	# Rate = 3.5
        	u = [29,3]
        elif M == 2 and Q == 4 and La == 1 and Lp == 16:
        	# Rate = 3.5
        	u = [21,59]
        elif M == 2 and Q == 4 and La == 4 and Lp == 8: # Rate = 4, maxp = 0.080042
        	u = [29,3]
        elif M == 2 and Q == 8 and La == 2 and Lp == 8: # Rate = 4, maxp = 0.0957012
        	u = [53,27]
        elif M == 2 and Q == 16 and La == 1 and Lp == 8: # Rate = 4, maxp = 0.109983
        	u = [51,81]
        elif M == 2 and Q == 8 and La == 1 and Lp == 16: # Rate = 4, maxp = 0.140074
        	u = [3,117]
        elif M == 2 and Q == 4 and La == 4 and Lp == 16: # Rate = 4.5
        	u = [7,57]
        elif M == 2 and Q == 8 and La == 4 and Lp == 16: # rate = 5, maxp = 0.0511476
        	u = [108,52]
        elif M == 2 and Q == 16 and La == 4 and Lp == 8: # rate = 5, maxp = 0.04216
        	u = [39,12]
        elif M == 2 and Q == 32 and La == 2 and Lp == 8: # rate = 5, maxp = 0.0483617
        	u = [242,46]
        elif M == 2 and Q == 8 and La == 8 and Lp == 16: # Rate = 5.5
        	u = [3,117]
        elif M == 2 and Q == 8 and La == 8 and Lp == 32: # Rate = 6
        	u = [11,237]
        elif M == 4 and Q == 1 and La == 1 and Lp == 2: # Rate = 0.75
        	u = [1,1,1,1]
        elif M == 4 and Q == 2 and La == 1 and Lp == 2: # Rate = 1
        	u = [1,1,3,3]
        elif M == 4 and Q == 2 and La == 1 and Lp == 4: # Rate = 1.25
        	u = [1,3,7,5]
        elif M == 4 and Q == 2 and La == 1 and Lp == 8: # Rate = 1.5
        	#u = [1,3,7,9]
        	u = [1,5,11,15]
        elif M == 4 and Q == 4 and La == 1 and Lp == 8: # Rate = 1.75
        	#u = [9,21,15,27]
        	u = [5,25,11,31]
        elif M == 4 and Q == 1 and La == 4 and Lp == 16: # rate = 2, maxp = 0.0712369
        	u = [0,0,0,0]
        elif M == 4 and Q == 1 and La == 1 and Lp == 64: # rate = 2, maxp = 0.0490677
        	u = [0,0,0,0]
        elif M == 4 and Q == 2 and La == 4 and Lp == 8: # rate = 2, maxp = 0.0969766
        	u = [2,13,3,14]
        elif M == 4 and Q == 2 and La == 1 and Lp == 32: # rate = 2, maxp = 0.0980171
        	u = [59,31,49,41]
        elif M == 4 and Q == 4 and La == 2 and Lp == 8: # rate = 2, maxp = 0.214639
        	u = [21,3,29,11]
        elif M == 4 and Q == 4 and La == 1 and Lp == 16: # rate = 2, maxp = 0.19509
        	u = [37,27,11,21]
        elif M == 4 and Q == 8 and La == 2 and Lp == 4: # rate = 2, maxp = 0.199766
        	u = [26,9,31,14]
        elif M == 4 and Q == 8 and La == 1 and Lp == 8: # rate = 2, maxp = 0.312322
        	u = [15,41,57,63]
        elif M == 4 and Q == 16 and La == 1 and Lp == 4: # rate = 2, maxp = 0.256578
        	u = [31,61,49,59]
        elif M == 4 and Q == 32 and La == 1 and Lp == 2: # rate = 2, maxp = 0.312322
        	u = [51,21,5,3]
        elif M == 4 and Q == 16 and La == 1 and Lp == 8: # Rate = 2.25
        	u = [21,37,91,83]
        elif M == 4 and Q == 8 and La == 8 and Lp == 16: # rate = 3, maxp = 0.0260332
        	u = [114,25,14,99]
        elif M == 4 and Q == 16 and La == 4 and Lp == 16: # rate = 3, maxp = 0.0546157
        	u = [97,145,236,25]
        elif M == 4 and Q == 32 and La == 4 and Lp == 8: # rate = 3, maxp = 0.0557874
        	u = [196,108,252,65]
        elif M == 4 and Q == 64 and La == 1 and Lp == 16: # Rate = 3
        	u = [633,603,559,797]
        elif M == 8 and Q == 1 and La == 2 and Lp == 8: # rate = 0.875, maxp = 0.24203
        	u = [0,0,0,0,0,0,0,0]
        elif M == 8 and Q == 2 and La == 2 and Lp == 4: # rate = 0.875, maxp = 0.298721
        	u = [1,1,7,2,7,6,1,7]
        elif M == 8 and Q == 4 and La == 1 and Lp == 4: # rate = 0.875, maxp = 0.522137
        	u = [9,11,3,7,15,13,5,1]
        elif M == 8 and Q == 2 and La == 2 and Lp == 8: # rate = 1, maxp = 0.24203
        	u = [9,1,1,15,14,1,15,10]
        elif M == 8 and Q == 4 and La == 2 and Lp == 4: # rate = 1, maxp = 0.262553
        	u = [1,11,2,11,14,5,5,15]
        elif M == 8 and Q == 8 and La == 1 and Lp == 4: # rate = 1, maxp = 0.375254
        	u = [25,31,15,13,7,1,17,3]
        elif M == 16 and Q == 64 and La == 1 and Lp == 1: # rate = 0.625, maxp = 0
        	u = [63,0,18,34,62,36,37,1,26,55,37,54,46,15,39,26]
        else:
        	print("TASTCode.py does not support the given parameters M = %d, Q = %d, La = %d, and Lp = %d" % (M, Q, La, Lp))
        	u = zeros(M)

        return np.array(u)

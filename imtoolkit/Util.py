# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

"""
Basic utility functions
"""
import os
import itertools
from sympy.combinatorics.graycode import GrayCode
from scipy.interpolate import interp1d
import numpy as np
if os.getenv("USECUPY") == "1":
    from cupy import *
    # print("cupy is imported by Util.py")
else:
    from numpy import *
    # print("numpy is imported by Util.py")


def getGrayIndixes(bitWidth):
    gray = GrayCode(bitWidth)
    return [int(strb, 2) for strb in gray.generate_gray()]

def frodiff(x, y):
    return power(linalg.norm(x - y), 2)

def getEuclideanDistances(symbols): 
    combsfro = itertools.starmap(frodiff, itertools.combinations(symbols, 2))
    return array(list(combsfro))

def getMinimumEuclideanDistance(symbols):
    return min(getEuclideanDistances(symbols))

def getDFTMatrix(N):
    W = zeros((N, N), dtype = complex)
    omega = exp(2.0j * pi / N)
    for j in range(N):
        for k in range(N):
            W[j, k] = pow(omega, j * k)
    W /= sqrt(N)
    return W

#
# IT++ like functions
#
def inv_dB(dB):
    return 10.0 ** (dB / 10.0)

def randn(*size):
    return random.normal(0, 1, size = size)

def randn_c(*size):
    """
    Complex normal distribution
    """
    return random.normal(0, 1 / sqrt(2.0), size = size) + random.normal(0, 1 / sqrt(2.0), size = size) * 1j
#xp.random.randn_c = randn_c


def countErrorBits(x, y):
    return bin(x^y).count('1')

def getXORtoErrorBitsArray(Nc):
    return array(list(map(lambda x: bin(x).count('1'), range(Nc + 1))))

def getErrorBitsTable(Nc):
    B = log2(Nc)
    errorArray = getXORtoErrorBitsArray(Nc)

    errorTable = zeros((Nc, Nc), dtype = int8)
    for y in range(Nc):
        for x in range(y, Nc):
            errorTable[y][x] = errorTable[x][y] = errorArray[x^y]
    
    return errorTable

def getXCorrespondingToY(xarr, yarr, y):
    if y < np.min(yarr) or y > np.max(yarr):
        return NaN
    spfunc = interp1d(yarr, xarr)
    return spfunc(y)


# c(APATH = "C:/Dropbox/Project/201903_imtoolkit_paper/paper/main.aux", label = "Conv. equiprobable act. \cite{wen2016equiprobable}")
# c(APATH = "C:/Dropbox/Project/201903_imtoolkit_paper/paper/main.aux", label = "Conv. SSK \cite{liu2015ssk}")
def c(APATH, label):
    import re
    with open(APATH, mode='r') as f:
        #
        chit = re.search(r'\\cite{(\S+)}', label)
        #print(chit)
        if chit == None:
            return label
        bibkey = chit.group(1)

        #
        ahit = re.search(bibkey + '}{(\d+)}', f.read())
        #print(ahit)
        if ahit:
            cn = ahit.group(1)
        else:
            cn = "?"
        
        return label.replace(chit.group(0), "[" + cn + "]")

def testUnitary(M, code):
    codes = code.codes.reshape(-1, M)
    np.testing.assert_almost_equal(np.conj(codes.T).dot(codes) / code.Nc, eye(M))

def getRandomHermitianMatrix(M):
    ret = diag(0j + randn(M))
    for y in range(0, M - 1):
        for x in range(y + 1, M):
            ret[y, x] = randn_c()
            ret[x, y] = conj(ret[y, x])
    return ret

def CayleyTransform(H):
    M = H.shape[0]
    return (eye(M, dtype=complex) - 1j * H).dot(linalg.inv(eye(M, dtype=complex) + 1j * H))

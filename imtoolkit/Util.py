# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import os
from sympy.combinatorics.graycode import GrayCode
from scipy.interpolate import interp1d
from scipy.constants import speed_of_light
from numba import jit, prange
import numpy as np
if os.getenv("USECUPY") == "1":
    import cupy as xp
else:
    import numpy as xp

@jit
def getGrayIndixes(bitWidth):
    gray = GrayCode(bitWidth)
    return [int(strb, 2) for strb in gray.generate_gray()]

def frodiff(x, y):
    return xp.square(xp.linalg.norm(x - y))

#@njit(['f8[:](c16[:,:,:])', 'f8[:](f8[:,:,:])']) # unknown type errors in some environments
@jit
def getEuclideanDistances(codes):
    # The following straightforward implementation with numba is the fastest
    Nc, M, T = codes.shape[0], codes.shape[1], codes.shape[2]
    tolBase = 2.22e-16 * max(M, T)

    ret = np.zeros(int(Nc * (Nc - 1) / 2))
    i = 0
    for y in prange(0, Nc):
        for x in range(y+1, Nc):
            diff = codes[y] - codes[x]
            _, s, _ = np.linalg.svd(diff.dot(np.conj(diff.T)))
            ret[i] = np.prod(s[s > tolBase])
            i += 1
    return ret

# The rank and determinant criterion
#@njit(['f8(c16[:,:,:])', 'f8(f8[:,:,:])']) # unknown type errors in some environments
def getMinimumEuclideanDistance(codes):
    # The following straightforward implementation with numba is the fastest
    Nc, M, T = codes.shape[0], codes.shape[1], codes.shape[2]
    tolBase = 2.22e-16 * max(M, T)
    mind = np.inf
    for y in prange(0, Nc):
        for x in range(y + 1, Nc):
            diff = codes[y] - codes[x]
            _, s, _ = np.linalg.svd(diff.dot(np.conj(diff.T)))
            d = np.prod(s[s > tolBase])
            if d < mind:
                mind = d
    return mind

def getDFTMatrix(N):
    W = xp.zeros((N, N), dtype = complex)
    omega = xp.exp(2.0j * xp.pi / N)
    for j in range(N):
        for k in range(N):
            W[j, k] = pow(omega, j * k)
    W /= xp.sqrt(N)
    return W

def getDFTMatrixNumpy(N):
    W = np.zeros((N, N), dtype = complex)
    omega = np.exp(2.0j * np.pi / N)
    for j in range(N):
        for k in range(N):
            W[j, k] = pow(omega, j * k)
    W /= np.sqrt(N)
    return W

#
# IT++ like functions
#
def inv_dB(dB):
    return 10.0 ** (dB / 10.0)

def randn(*size):
    return xp.random.normal(0, 1, size = size)

def randn_c(*size):
    """
    Complex normal distribution
    """
    return xp.random.normal(0, 1 / xp.sqrt(2.0), size = size) + xp.random.normal(0, 1 / xp.sqrt(2.0), size = size) * 1j
#xp.random.randn_c = randn_c

def countErrorBits(x, y):
    return bin(x^y).count('1')

def getXORtoErrorBitsArray(Nc):
    #return xp.array(list(map(lambda x: bin(x).count('1'), range(Nc + 1))))
    ret = xp.zeros(Nc + 1)
    for x in range(Nc + 1):
        ret[x] = bin(x).count('1')

    return ret

def getErrorBitsTable(Nc):
    errorArray = getXORtoErrorBitsArray(Nc)
    errorTable = xp.zeros((Nc, Nc), dtype = xp.int8)
    for y in range(Nc):
        for x in range(y, Nc):
            errorTable[y][x] = errorTable[x][y] = errorArray[x^y]
    
    return errorTable

def getXCorrespondingToY(xarr, yarr, y):
    if y < np.min(yarr) or y > np.max(yarr):
        return xp.NaN
    spfunc = interp1d(yarr, xarr)
    return spfunc(y)


# c(APATH = "C:/Dropbox/Project/201903_imtoolkit_paper/paper/main.aux", label = "Conv. equiprobable act. \cite{wen2016equiprobable}")
# c(APATH = "C:/Dropbox/Project/201903_imtoolkit_paper/paper/main.aux", label = "Conv. SSK \cite{liu2015ssk}")
def c(APATH, label):
    import re
    if not os.path.exists(APATH):
        return label

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

def testUnitaryCode(M, code):
    codes = code.codes.reshape(-1, M)
    np.testing.assert_almost_equal(np.conj(codes.T).dot(codes) / code.Nc, xp.eye(M))

def getRandomHermitianMatrix(M):
    ret = xp.diag(0j + randn(M))
    for y in range(0, M - 1):
        for x in range(y + 1, M):
            ret[y, x] = randn_c()
            ret[x, y] = xp.conj(ret[y, x])
    return ret

# TODO: need to support cp
def CayleyTransform(H):
    M = H.shape[0]
    I = np.eye(M, dtype=np.complex)
    U = np.matmul(I - 1.j * H, np.linalg.inv(I + 1.j * H))
    #U = np.matmul(H - 1.j * I, np.linalg.inv(H + 1.j * I))
    return U

# TODO: need to support cp
def CayleyTransformInv(U):
    M = U.shape[0]
    I = np.eye(M, dtype=np.complex)
    #H = 1.j * np.matmul(I + U,np.linalg.inv(I - U))
    H = -1.j * np.matmul(np.linalg.inv(I + U), I - U)
    return H

def asnumpy(xparr):
    if 'cupy' in str(type(xparr)):
        return xp.asnumpy(xparr) # cupy to numpy
    return xparr # do nothing

def ascupy(nparr):
    if 'numpy' in str(type(nparr)):
        return xp.asarray(nparr) # numpy to cupy
    return nparr # do nothing

# frequency [Hz], wavelength [m]
def frequencyToWavelength(frequency):
    return speed_of_light / frequency

def kurtosis(x):
    mu = xp.mean(x)
    mu2 = xp.mean(xp.power(x - mu, 2))
    mu4 = xp.mean(xp.power(x - mu, 4))
    beta2 = mu4 / (mu2 * mu2) - 3.0
    return beta2

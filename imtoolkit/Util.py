# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

"""
Basic utility functions
"""
import os
import itertools
from sympy.combinatorics.graycode import GrayCode
import importlib
import numpy as np
if os.getenv("USECUPY") == "1" and importlib.util.find_spec("cupy") != None:
    from cupy import *
    print("cupy is imported by Util.py")
else:
    from numpy import *
    print("numpy is imported by Util.py")


def getGrayIndixes(bitWidth):
    gray = GrayCode(bitWidth)
    return [int(strb, 2) for strb in gray.generate_gray()]

def frodiff(x, y):
    return power(linalg.norm(x - y), 2)

def getEuclideanDistances(symbols): 
    combsfro = itertools.starmap(frodiff, itertools.combinations(symbols, 2))
    return array(list(combsfro))


def getMinimumEuclideanDistance(symbols):
    # symbols = np.array([+1, -1, +1j, -1j])
    return min(getEuclideanDistances(symbols))

    ## old inefficient code
    #minmed = 1e3
    #for i in range(1, len(symbols)):
    #    diffs = symbols[0:-i] - symbols[-i]
    #    med = np.min(np.power(np.abs(diffs), 2))
    #    minmed = min(minmed, med)
    #
    #return minmed


#
# IT++ like functions
#
def inv_dB(dB):
    return 10.0 ** (dB / 10.0)
# inv_dB.inspect_types()

def randn_c(*size):
    """
    Complex normal distribution
    """
    return random.normal(0, 1 / sqrt(2.0), size = size) + random.normal(0, 1 / sqrt(2.0), size = size) * 1j
#xp.random.randn_c = randn_c



# countErrorBits(1, 2) #=> 2
# countErrorBits(1, 5) #=> 1
def countErrorBits(x, y):
    return binary_repr(int(bitwise_xor(x, y))).count('1')

def getErrorBitsTable(Nc):
    B = log2(Nc)
    errorTable = zeros((Nc, Nc), dtype = int32)

    for y in range(Nc):
        for x in range(y, Nc):
            errorTable[y][x] = errorTable[x][y] = countErrorBits(y, x)
    
    return errorTable

# NumPy domain
def getXORtoErrorBitsArray(Nc):
    ret = zeros(Nc, int32)
    for i in range(Nc):
        ret[i] = binary_repr(i).count('1')
    return ret

# getXORtoErrorBitsArray(4) # array([0, 1, 1, 2])
# getXORtoErrorBitsArray(16) # array([0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4])


from scipy.interpolate import interp1d
def getXCorrespondingToY(xarr, yarr, y):
    if y < np.min(yarr) or y > np.max(yarr):
        return NaN
    #print(where(y <= yarr))
    #print(where(y > yarr))
    spfunc = interp1d(yarr, xarr)
    return spfunc(y)

# getXCorrespondingToY(array([0,1]), array([0,1]), 0.5) # array(0.5)
# getXCorrespondingToY(array([0,1]), array([0,1]), [0.1,0.5]) # array([0.1, 0.5])


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
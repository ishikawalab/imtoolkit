# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import re
import glob
import itertools
import urllib.request
import numpy as np
from scipy import special
from numba import jit
from .Util import *

# Optimized indexes set in terms of AMI
INDS = {}
INDS[2, 1, 2] = [[0], [1]]
INDS[4, 2, 2] = [[0, 1], [0, 2]] # 
#INDS[4, 2, 2] = [[0, 1], [2, 3]] # 
INDS[4, 2, 4] = [[0, 1], [0, 2], [1, 3], [2, 3]] # 


#
# Utility functions for an indexes set
#

#
# inds = [[0, 1], [0, 2]]; M = 4
# return: [array([[1], [1], [0], [0]]), array([[1], [0], [1], [0]])]
#
def convertIndsToVector(inds, M):
    Q = len(inds)
    ret = np.tile(np.zeros((M, 1), dtype=np.int32), Q) # M \times Q matrix
    for q in range(Q):
        for i in inds[q]:
            ret[i][q] = 1
    return np.hsplit(ret, Q)

#
# inds = [[0, 1], [0, 2]]; M = 4
# return: [array([[1., 0.], [0., 1.], [0., 0.], [0., 0.]]), array([[1., 0.], [0., 0.], [0., 1.], [0., 0.]])]
# 
def convertIndsToMatrix(inds, M):
    Q = len(inds)
    K = len(inds[0])
    ret = np.tile(np.zeros((M, K)), Q)

    t = 0
    for q in range(Q):
        for i in inds[q]:
            ret[i][t] = 1
            t += 1
    return np.hsplit(ret, Q)

def convertIndsToIndsDec(inds, M):
    ret = []
    for row in inds:
        dec = np.sum(np.power(2, row))
        ret.append(dec)
    return ret

# convertIndsDecToInds(indsdecs = [3,5,10,12], M = 4) # [[0, 1], [0, 2], [1, 3], [2, 3]]
def convertIndsDecToInds(indsdecs, M):
    Q = len(indsdecs)
    ret = []
    for dec in indsdecs:
        binstr = np.binary_repr(dec)
        binstr = '0' * (M - len(binstr)) + binstr
        binstr = binstr[::-1]
        ind = []
        for i in range(len(binstr)):
            if binstr[i] == '1':
                ind.append(i)
        ret.append(ind)
    return ret

def outputIndsToFile(inds, M):
    Q = len(inds)
    K = len(inds[0])
    minh = getMinimumHammingDistance(inds, M)
    ineq = getInequalityL1(inds, M)

    basePath = os.path.dirname(os.path.abspath(__file__))
    fname = basePath + "/inds/M=%d_K=%d_Q=%d_minh=%d_ineq=%d.txt" % (M, K, Q, minh, ineq)
    np.savetxt(fname, inds, fmt = "%.0d")
    print("Saved to " + fname)
    return fname


# Usage: convertIndsToMatrix(getDictionaryIndexesList(M, K, Q), M)
def getDictionaryIndexesList(M, K, Q):
    ret = [list(l) for l in itertools.combinations(range(M), K)]
    maxQ = int(np.exp2(np.floor(np.log2(len(ret)))))

    if Q > maxQ:
        print("The given Q is larger than the maximum:" + str(Q) + " > " + str(maxQ))
        return ret[0:maxQ]

    return ret[0:Q]

# This method is based on the Matlab implementation for the GSM scheme,
# which is given by the following book.
# R. Mesleh and A. Alhassi, Space modulation techniques. Wiley, 2018.
def getMeslehIndexesList(M, K, Q):
    ret = [list(l) for l in reversed(list(itertools.combinations(range(M), K)))]
    maxQ = int(np.exp2(np.floor(np.log2(len(ret)))))

    if Q > maxQ:
        print("The given Q is larger than the maximum:" + str(Q) + " > " + str(maxQ))
        return ret[0:maxQ]

    return ret[0:Q]

# M. Wen, Y. Zhang, J. Li, E. Basar, and F. Chen,
# ``Equiprobable subcarrier activation method for OFDM with index modulation,''
# IEEE Commun. Lett., vol. 20, no. 12, pp. 2386--2389, 2016.
def wen2016EquiprobableSubcarrierActivation(M, K):
    # initialize an indexes set ds
    ds = [np.ones(K, dtype=np.int)]
    ds[0][K - 1] = M - K + 1
    
    if K >= 2:
        j = K - 2
        b = 1
        while True:
            while True:
                d = np.copy(ds[b - 1])
                d[j] += 1
                d[range(j + 1, K - 1)] = 1
                d[K - 1] = 0
                d[K - 1] = M - np.sum(d)
                if d[K - 1] < 1:
                    j -= 1
                else:
                    break
            
            if d[0] > M / K:
                break
            
            ds.append(d)
            b += 1

    # delete cyclic shifts in ds
    deletepos = []
    for y in range(len(ds)):
        if y in deletepos:
            continue
        for x in range(y + 1, len(ds)):
            if x in deletepos:
                continue
            for i in range(K):
                if np.array_equal(ds[y], np.roll(ds[x], i)):
                    deletepos.append(x)
                    break
    ds = np.delete(ds, deletepos, axis = 0)
    # print(deletepos)
    # print(ds)

    # build an indexes set from ds
    betas = []
    for i in range(len(ds)):
        for m in range(M):
            beta = [0] * K
            beta[0] = m
            for k in range(1, K):
                beta[k] = (beta[k - 1] + 1 + ds[i][k - 1] - 1)%M
            beta = sorted(beta)
            if beta not in betas:
                betas.append(beta)
    
    #print(len(betas))
    Qmax = int(M * np.floor(len(betas) / M))
    #print("Q = " + str(Q))

    return betas[0:Qmax]

def getRandomIndexesList(M, K, Q):
    ret = []
    while len(ret) < Q:
        row = sorted(np.random.choice(M, K, replace = False))
        if row not in ret:
            ret.append(row)
    return ret

def downloadOptimizedIndexesList(basePath, M, K, Q, source):
    print("Trying to obtain the active indices file from " + source + ".")
    txtfilename = "M=%d_K=%d_Q=%d.txt" % (M, K, Q)
    txtdstpath = basePath + "/inds/" + txtfilename

    if not os.path.exists(basePath + "/inds/"):
        os.mkdir(basePath + "/inds/")

    if source == "GitHub":
        txturl = "https://raw.githubusercontent.com/imtoolkit/imtoolkit/master/docs/build/html/db/M=" + str(M) + "/" + txtfilename
    else:
        txturl = "https://ishikawa.cc/imtoolkit/db/M=" + str(M) + "/" + txtfilename
    
    try:
        urllib.request.urlretrieve(txturl, txtdstpath)
    except:
        print("Perhaps...")
        print("    " + source + " is currently not available.")
        print("    You need the root permission.")
        print("    The specified IM parameters are invalid or not supported.")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def getOptimizedIndexesList(M, K, Q, minh = 0):
    basePath = os.path.dirname(os.path.abspath(__file__))

    if minh == 0:
        files = glob.glob(basePath + "/inds/M=%d_K=%d_Q=%d.txt"%(M, K, Q))
        files += glob.glob(basePath + "/inds/M=%d_K=%d_Q=%d_*.txt"%(M, K, Q))
    else:
        files = glob.glob(basePath + "/inds/M=%d_K=%d_Q=%d_minh=%d*.txt"%(M, K, Q, minh))

    # download the active indices from some webpages
    if len(files) == 0:
        if not downloadOptimizedIndexesList(basePath, M, K, Q, "GitHub"):
            downloadOptimizedIndexesList(basePath, M, K, Q, "ishikawa.cc")
        
        files = glob.glob(basePath + "/inds/M=%d_K=%d_Q=%d.txt"%(M, K, Q))
        if len(files) == 0:
            print("No file found.")
            return []

    files.sort()
    print("Read " + files[0])
    inds = np.loadtxt(files[0], dtype = np.int)
    print(inds)
    inds = inds.reshape(Q, K).tolist()
    return inds

def getIndexes(type, M, K, Q):
    if "opt" in type:
        minh = int(type.replace("opt", "0"))
        inds = getOptimizedIndexesList(M, K, Q, minh)
    elif type == "dic":
        inds = getDictionaryIndexesList(M, K, Q)
    elif type == "mes":
        inds = getMeslehIndexesList(M, K, Q)
    elif type == "wen":
        inds = wen2016EquiprobableSubcarrierActivation(M, K)
        if Q > len(inds):
            print("The specified Q = %d is not supported by wen2016 algorithm" % (Q))
            return []
        inds = inds[0:Q]
        #print("Q is automatically set to " + str(len(inds)))
    elif type == "rand":
        inds = getRandomIndexesList(M, K, Q)
    elif type == "ga": # Genetic algorithm aided design
        if M == 16 and K == 8 and Q == 16:
            inds = [
                [0, 1, 2, 4,  7,  8, 11, 15],
                [0, 1, 2, 4, 10, 13, 14, 15],
                [0, 2, 3, 4,  6,  7, 12, 14],
                [0, 2, 4, 5,  6,  8, 11, 12],
                [0, 2, 5, 8, 10, 11, 13, 15],
                [0, 3, 4, 5,  6,  9, 11, 15],
                [0, 3, 4, 7, 10, 11, 13, 15],
                [0, 3, 7, 8,  9, 10, 13, 14],
                [1, 2, 3, 9, 10, 12, 13, 15],
                [1, 2, 6, 9, 10, 11, 12, 14],
                [1, 3, 5, 6,  7,  8, 11, 13],
                [1, 4, 5, 7,  8, 12, 13, 14],
                [1, 4, 5, 8,  9, 10, 14, 15],
                [1, 5, 6, 7,  9, 10, 12, 15],
                [2, 3, 5, 6,  8,  9, 12, 14],
                [3, 6, 7, 9, 11, 12, 13, 14]]
    else:
        print("Error: The type of active indices is not specified.")
    
    if len(inds) == 0:
        print("The specified indexes set is not available.")
        return []
    
    return inds

#
# Evaluation functions
#
def getProbabilityOfActivation(inds, M):
    prob = np.zeros(M)
    for q in range(len(inds)):
        prob[inds[q]] += 1
    return prob / len(inds)

#
# getHammingDistance([0,1], [1,0]) = 2
# getHammingDistance([1,1,0,0], [0,0,1,1]) = 4
@jit
def getHammingDistance(arr1, arr2):
    return np.sum(np.logical_xor(arr1, arr2))

def getMinimumHammingDistance(inds, M):
    Q = len(inds)
    indsm = convertIndsToVector(inds, M)
    mind = M + 1
    for y in range(Q):
        for x in range(y + 1, Q):
            hammingdis = np.sum(np.logical_xor(indsm[y].reshape(M), indsm[x].reshape(M)))
            if hammingdis < mind:
                mind = hammingdis
    return mind

def getSumHamming(inds, M):
    Q = len(inds)
    indsm = convertIndsToVector(inds, M)
    ret = 0
    for y in range(Q):
        for x in range(y + 1, Q):
            hammingdis = np.sum(np.logical_xor(indsm[y].reshape(M), indsm[x].reshape(M)))
            ret += hammingdis
    return ret

def getSumDistanceBetweenActivatedElements(inds, M):
    Q = len(inds)
    ret = 0
    for q in range(Q):
        ret += np.sum(np.diff(inds[q]) - 1)
    return ret

# getInequalityL1(inds = [[0,1],[2,3]], M = 4) # = 0.0
def getInequalityL1(inds, M):
    Q = len(inds)
    K = len(inds[0])
    hits = np.zeros(M)
    for q in range(len(inds)):
        hits[inds[q]] += 1
    return np.sum(np.abs(hits - Q * K / M))

def checkConflict(inds):
    Q = len(inds)
    for y in range(Q):
        for x in range(y + 1, Q):
            if np.array_equal(inds[y], inds[x]):
                print("Conflicted " + "-" * 20)
                print("y = " + str(y) + ":" + str(inds[y]))
                print("x = " + str(x) + ":" + str(inds[x]))
                return True
    return False

#
# Others
#

def getIMParameters(M, K):
    ret = []
    Qmax = int(np.exp2(np.floor(np.log2(special.binom(M, K)))))
    if Qmax == 1:
        return ret
    Q = 2
    while Q <= Qmax:
        ret.append((M, K, Q))
        Q *= 2
    return ret

# getIMParameters(4, 2) # [(4, 2, 1), (4, 2, 2), (4, 2, 4)]

def binom(M,K):
    return special.binom(M, K)


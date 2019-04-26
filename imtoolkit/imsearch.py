# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import os
import sys
import glob
import re
import time
from scipy import special
import numpy as np
import itertools
from numba import jit
from imtoolkit import *

@jit
def getHammingDistanceTable(MCK, indsdec):
    # This method is not dependent on Q
    hds = np.zeros((MCK, MCK), dtype = np.int) 
    imax = MCK * (MCK - 1) / 2
    i = 0
    for y in range(MCK):
        for x in range(y + 1, MCK):
            hammingdis = countErrorBits(indsdec[y], indsdec[x])
            hds[y][x] = hds[x][y] = hammingdis
            i += 1
        print("%.3f percent completed." % (i / imax * 100.0))
    return hds

@jit
def getGoodDecsTable(M, K):
    inds = list(itertools.combinations(range(M), K))
    indsv = convertIndsToVector(inds, M)
    indsdec = convertIndsToIndsDec(inds, M)
    MCK = len(inds)
    hds = np.zeros((MCK, MCK), dtype = np.int) # This is not dependent on Q

    minHT = 4
    newdecs = {}
    for x in range(1, MCK):
        hds[0][x] = np.sum(np.logical_xor(indsv[0].reshape(M), indsv[x].reshape(M)))
    #print(hds[0])
    while True:
        gooddecs = where(hds[0] >= minHT)[0].tolist()
        if len(gooddecs) == 0:
            break
        
        print("minHT = %d" % (minHT))
        newdecs[minHT] = [0]
        newdecs[minHT].extend(gooddecs)
        #print("extended")
        #print(newdecs)
        
        lennd = len(newdecs[minHT])
        deletepos = []
        for y in range(1, lennd):
            if y in deletepos:
                continue
            yp = newdecs[minHT][y]
            for x in range(y + 1, lennd):
                if x in deletepos:
                    continue
                xp = newdecs[minHT][x]
                if hds[yp][xp] == 0:
                    hds[yp][xp] = np.sum(np.logical_xor(indsv[yp].reshape(M), indsv[xp].reshape(M)))
                if hds[yp][xp] < minHT:
                    deletepos.append(x)
            print("%.2f percent" % (100.0 * y / lennd))
        newdecs[minHT] = np.delete(newdecs[minHT], deletepos, axis = 0)
        if len(newdecs[minHT]) <= 1:
            del newdecs[minHT]
            break
        newdecs[minHT] = np.take(indsdec, newdecs[minHT]).tolist()
        #print("deleted")
        #print(newdecs)
        #print(getMinimumHamming(convertIndsDecToInds(newdecs[minHT], M), M))
        
        if len(newdecs[minHT]) == 0:
            break
        minHT += 2
        
        #print("%.3f percent completed." % (i / imax * 100.0))
    return newdecs

@jit
def getGoodDecsTableSmallMemory(M, K):
    minHT = 4
    indsiter = itertools.combinations(range(M), K)
    firstivec = np.zeros(M, dtype=np.int)
    firstind = np.array(next(indsiter))
    firstivec[firstind] = 1
    #print(firstivec)
    firstdec = np.sum(np.power(2, firstind))

    # Extracts the active indices having minHT >= 4
    indsvec = [firstivec]
    indsdec = [firstdec]
    for ind in indsiter:
        ivec = np.zeros(M, dtype=np.int)
        npind = np.array(ind)
        ivec[npind] = 1
        hd = np.sum(np.logical_xor(firstivec, ivec))
        if hd < minHT:
            continue
        indsvec.append(ivec)
        indsdec.append(np.sum(np.power(2, npind)))
    
    #print(indsdec)
    #print(len(indsvec))
    #print(len(indsdec))

    MCK = len(indsvec)
    newdecs = {}
    while True:
        print("minHT = %d" % (minHT))
        newdecs[minHT] = indsdec
        #print(newdecs)
        
        lennd = len(newdecs[minHT])
        lstart = 0
        if minHT == 4:
            lstart = 1
        deletepos = []
        for y in range(lstart, lennd):
            if y in deletepos:
                continue
            for x in range(y + 1, lennd):
                if x in deletepos:
                    continue
                hd = np.sum(np.logical_xor(indsvec[y], indsvec[x]))
                if hd < minHT:
                    deletepos.append(x)
            print("%.2f percent" % (100.0 * y / lennd))
        #print(deletepos)
        newdecs[minHT] = list(np.delete(newdecs[minHT], deletepos, axis = 0))
        if len(newdecs[minHT]) <= 1:
            del newdecs[minHT]
            break
        
        if len(newdecs[minHT]) == 0:
            break
        minHT += 2

    return newdecs

def getAllIndsBasedOnDecFile(M, K, Q):
    basePath = os.path.dirname(os.path.abspath(__file__))
    decfilename = basePath + "/decs/M=%d_K=%d.txt" % (M, K)
    if os.path.exists(decfilename):
        with open(decfilename, mode = 'r') as f:
            decs = eval(f.read())
            #print(decs)
            print("Read " + decfilename)

            minh = 0
            for key in decs.keys():
                if Q <= len(decs[key]):
                    minh = key
            print(minh)
            if minh > 0:
                return convertIndsDecToInds(decs[minh], M)
    return []

def outputCPLEXModelFile(M, K, Q):
    #print("MCK = " + str(MCK))
    allinds = list(itertools.combinations(range(M), K))
    allindsvec = convertIndsToVector(allinds, M)
    allindsmat = np.hstack(allindsvec).T.tolist() # MCK \times M
    MCK = len(allindsmat)
    #print("allinds generated.")

    constraints = []

    decallinds = getAllIndsBasedOnDecFile(M, K, Q)
    if len(decallinds) > 0:
        allinds = decallinds
        #print(getMinimumHamming(allinds, M))
        allindsvec = convertIndsToVector(allinds, M)
        allindsmat = np.hstack(allindsvec).T.tolist() # MCK \times M
        MCK = len(allindsmat)
    
    constraints.append("    a[1] == 1;\n")
    
    #
    #indsv = convertIndsToVector(allinds, M)
    #print(getGoodDecsTable(MCK, indsdec))
    #print("hds generated.")

    basePath = os.path.dirname(os.path.abspath(__file__))
    fname = basePath + "/inds-raw/M=%d_K=%d_Q=%d.mod" % (M, K, Q)
    with open(fname, mode = 'w') as f:
        f.write("int M=%d; int K=%d; int Q=%d; int MCK=%d;\n" % (M, K, Q, MCK))
        f.write("int allinds[1..MCK][1..M] = " + str(allindsmat) + ";\n\n")
        f.write("dvar boolean a[1..MCK];\n\n")
        #
        f.write("execute PARAMS {\n")
        f.write("    cplex.mipemphasis = 0;\n")
        f.write("    cplex.tilim = 60 * 60;\n")
        f.write("    cplex.mipdisplay = 3;\n")
        f.write("}\n\n")
        #
        f.write("minimize sum(m in 1..M) (abs(sum(q in 1..MCK)(a[q] * allinds[q][m]) - (Q * K / M)));\n\n")
        #
        f.write("subject to{\n")
        # add constraints
        f.writelines(constraints)
        f.write("    sum(q in 1..MCK)(a[q]) == Q;\n")
        f.write("}\n\n")
        #
        f.write("execute{\n")
        f.write("    var f = new IloOplOutputFile(\"M=\" + M + \"_K=\"+ K + \"_Q=\" + Q + \"_obj=\" + cplex.getObjValue() + \".txt\");\n")
        f.write("    f.write(a);\n")
        f.write("    f.close();\n")
        f.write("}\n")
    
    print("Saved to " + fname)
    return fname


def convertCPLEXOutputToInds(fname, M, K, Q):
    allinds = np.array(list(itertools.combinations(range(M), K)))
    decallinds = getAllIndsBasedOnDecFile(M, K, Q)
    if len(decallinds) > 0:
        allinds = decallinds

    with open(fname, mode='r') as f:
        content = f.read()
        content = re.sub(r'\s+', ' ', content)
        content = re.sub(r'^\s+', '', content)
        content = re.sub(r'\n', '', content)
        content = content.replace(" ", ",")
        #print(content)
        inds = np.array(eval(content))
        #print(inds)
        #print(np.nonzero(inds)[0].tolist())
        inds = np.take(allinds, np.nonzero(inds)[0], axis = 0)
        return inds

def main():
    if len(sys.argv) <= 1:
        print("DECPARAMS_M=32")
        print("DECPARAMSDO_M=32")
        print("SEARCHPARAMS_M=32")
        print("SEARCHPARAMSDO_M=32")
        print("SEARCH_M=2_K=1_Q=2")
        print("SEARCH_M=4_K=1_Q=2")
        print("EVAL_dm=dic_M=2_K=1_Q=2")
        print("EVAL_dm=dic_M=16_K=8_Q=16")
        print("EVAL_dm=mes_M=16_K=8_Q=16")
        print("EVAL_dm=wen_M=16_K=8_Q=16")
        print("DECSEARCH_M=4_K=2")
        print("DECEVAL_M=4_K=2")
        print("DECSEARCH_M=8_K=4")
        print("DECEVAL_M=8_K=4")
        print("DECSEARCH_M=16_K=8")
        print("DECEVAL_M=16_K=8")
        print("MINH")
        quit()

    args = sys.argv[1:]
    for arg in args:
        print("-" * 50)
        print("arg = " + arg)
        params = Parameters(arg)
        basePath = os.path.dirname(os.path.abspath(__file__))

        start_time = time.time()
        if params.mode == "SEARCHPARAMS" or params.mode == "SEARCHPARAMSDO":
            imparams = []
            allpossibleparams = 0
            M = 2
            while True:
                for K in range(1, M):
                    ps = getIMParameters(M, K)
                    for p in ps:
                        fpy = glob.glob(basePath + "/inds/M=%d_K=%d_Q=%d*.txt" % (p[0], p[1], p[2]))
                        allpossibleparams += 1
                        if len(fpy) == 0:
                            imparams.append(p)
                M += 2
                if M > params.M:
                    break
            print("Search coverage = %.2f percent" % (100.0 - 100.0 * len(imparams) / allpossibleparams))
            imparams.sort(key = lambda x:x[2])
            cmds = []
            for p in imparams:
                cmd = "imsearch SEARCH_M=%d_K=%d_Q=%d" % (p[0], p[1], p[2])
                cmds.append(cmd)
                print(cmd)
            if params.mode == "SEARCHPARAMSDO":
                for cmd in cmds:
                    os.system(cmd)

        elif params.mode == "DECPARAMS" or params.mode == "DECPARAMSDO":
            decparams = []
            allpossibleparams = 0
            M = 2
            while True:
                for K in range(2, M - 1): # excludes K = 1 and K = M - 1
                    decfilename = basePath + "/decs/M=%d_K=%d.txt" % (M, K)
                    if not os.path.exists(decfilename):
                        decparams.append([M, K])
                    allpossibleparams += 1
                M += 2
                if M > params.M:
                    break
            print("Search coverage = %.2f percent" % (100.0 - 100.0 * len(decparams) / allpossibleparams))
            decparams.sort(key = lambda x:special.binom(x[0], x[1]))
            cmd = "echo " + " ".join(["DECSEARCH_M=%d_K=%d" % (p[0], p[1]) for p in decparams]) + " | xargs -n1 -P15 imsearch"
            if params.mode == "DECPARAMSDO":
                os.system(cmd)
            else:
                print(cmd)

        elif params.mode == "DECSEARCH":                        
            #dectable = getGoodDecsTable(params.M, params.K)
            dectable = getGoodDecsTableSmallMemory(params.M, params.K)
            decfilename = basePath + "/decs/M=%d_K=%d_option=low.txt" % (params.M, params.K)
            with open(decfilename, mode = 'w') as f:
                f.write(str(dectable))
            print("Saved to " + decfilename)

        elif params.mode == "DECEVAL":
            decfilename = basePath + "/decs/M=%d_K=%d.txt" % (params.M, params.K)
            with open(decfilename, mode = 'r') as f:
                print("Read " + decfilename)
                dectable = eval(f.read())
                print(dectable)
                for minh in dectable.keys():
                    print("minh = %d" % (minh))
                    allinds = convertIndsDecToInds(dectable[minh], params.M)
                    print(allinds)
                    print("actual minh = %d" % (getMinimumHammingDistance(allinds, params.M)))
           
        elif params.mode == "SEARCH":
            fname = outputCPLEXModelFile(params.M, params.K, params.Q)
            if ".mod" in fname:
                os.system("oplrun " + fname)
                # Convert the obtained solution to a numpy file
                fcout = glob.glob(basePath + "/inds-raw/M=%d_K=%d_Q=%d*.txt" % (params.M, params.K, params.Q))
                if len(fcout) > 0:
                    fcout.sort()
                    fname = fcout[0]
                    obj = 0
                    if "obj=" in fname:
                        res = re.match(r'.*_obj=(\d+)', fname)
                        if res:
                            obj = int(res.group(1))
                    inds = convertCPLEXOutputToInds(fname, params.M, params.K, params.Q)
                    outputIndsToFile(inds, params.M)

        elif params.mode == "EVAL":
            inds = getIndexes(params.dm, params.M, params.K, params.Q)
            print(np.array(convertIndsToVector(inds, params.M)).reshape(-1, params.Q))
            print("Minimum Hamming distance = %d" % getMinimumHammingDistance(inds, params.M))
            print("Inequality L1 = %d" % getInequalityL1(inds, params.M))
        elif params.mode == "VIEWH":
            np.set_printoptions(threshold=np.inf)
            M = params.M
            titlestr = "M = %d" % M

            def lfs(f):
                fn = os.path.basename(f).replace(".txt", "")
                p = Parameters(fn)
                return (p.M * 32 + p.K) * 10000000 + p.Q

            files = glob.glob(basePath + "/inds/M=%d_*.txt" % M)
            files.sort(key = lfs)

            def numpyToPythonStr(numpystr):
                return numpystr.replace(".", "").replace("  ", " ").replace("\n\n", "\n").replace("\n ", ", ").replace(" 0", ", 0").replace(" 1", ", 1")


            print("")
            print("=" * len(titlestr))
            print(titlestr)
            print("=" * len(titlestr))
            print("")
           
            for f in files:
                fn = os.path.basename(f).replace(".txt", "")
                p = Parameters(fn)
                inds = np.loadtxt(f, dtype = np.int)
                inds = inds.reshape(p.Q, p.K).tolist()

                at = np.array(convertIndsToMatrix(inds, M))
                ats = numpyToPythonStr(str(at))
                vrstr = numpyToPythonStr(str(np.array(convertIndsToVector(inds, M)).reshape(-1, p.M)))
                vrstr = vrstr.replace("], ", "],\n     ")
                
                ts = fn.replace("M=%d_"%M, "").replace("_minh=%d"%p["minh"], "").replace("_ineq=%d"%p["ineq"], "").replace("_", ", ").replace("=", " = ")
                print(ts)
                print("-" * len(ts))
                print(".. code-block:: python\n")
                print("    # minimum Hamming distance = %d" % p["minh"])
                print("    # activation inequality = %d" % p["ineq"])
                print("    # active indices")
                print("    a = " + str(inds))
                print("    # activation tensor")
                print("    A = " + ats)
                print("    # vector representation")
                print("    " + vrstr)
                print("")
            
        elapsed_time = time.time() - start_time
        print ("Elapsed time = %.10f seconds" % (elapsed_time))


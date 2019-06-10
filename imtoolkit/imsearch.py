# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import os
import sys
import glob
import re
import time
import shutil
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

#@jit
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
        hd = getHammingDistance(firstivec, ivec)
        if hd < minHT:
            continue
        indsvec.append(ivec)
        indsdec.append(np.sum(np.power(2, npind)))
    
    indsvec = np.array(indsvec)
    #print(np.take(indsvec, np.array([0, 1]), axis=0))
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

        ys = np.array(list(range(lstart, lennd)))
        #print(ys)
        #for y in range(lstart, lennd):
        yi = 0
        y = ys[yi]
        while True:
            #if y in deletepos:
            #    continue

            xs = np.array(list(range(y + 1, lennd)))
            #print(xs)
            #print(deletepos)
            xs = np.setdiff1d(xs, deletepos)
            if len(xs) > 0:
                #print(indsvec[xs])
                vxs = np.take(indsvec, xs, axis = 0)
                #print(vxs.shape)
                #print(vxs)
                vys = np.tile(indsvec[y], len(xs)).reshape(-1, M)
                #print(vys)
                hds = np.sum(np.logical_xor(vxs, vys), axis = 1)
                #hds = np.apply_along_axis(lambda x: getHammingDistance(indsvec[y], indsvec[x[0]]), 0, xs.reshape(1, len(xs)))
                #print(hds)
                #print(list(np.where(hds < minHT)[0]))
                newdel = list(xs[np.where(hds < minHT)[0]])
                deletepos.extend(newdel)
                ys = np.setdiff1d(ys, newdel)
            #print(ys)
            #for x in range(y + 1, lennd):
            #    if x in deletepos:
            #        continue
            #    hd = np.sum(np.logical_xor(indsvec[y], indsvec[x]))
            #    if hd < minHT:
            #        deletepos.append(x)
            print("%.2f percent" % (100.0 * y / lennd))
            yi += 1
            if yi >= len(ys):
                break
            y = ys[yi]
        
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
    return None

def outputCPLEXModelFile(M, K, Q):
    decallinds = getAllIndsBasedOnDecFile(M, K, Q)
    if K > 1 and K < M-1 and decallinds == None:
        print("The dec file for (%d,%d) does not exist." % (M,K))
        return None

    if decallinds != None and len(decallinds) > 0:
        allinds = decallinds
        #print(getMinimumHamming(allinds, M))
        allindsvec = convertIndsToVector(allinds, M)
        allindsmat = np.hstack(allindsvec).T.tolist() # MCK \times M
        MCK = len(allindsmat)
    else:
        allinds = list(itertools.combinations(range(M), K))
        allindsvec = convertIndsToVector(allinds, M)
        allindsmat = np.hstack(allindsvec).T.tolist() # MCK \times M
        MCK = len(allindsmat)
    
    constraints = ["    a[1] == 1;\n"]
    
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
    if decallinds != None and len(decallinds) > 0:
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

def numpyToPythonStr(numpystr):
    return numpystr.replace(".", "").replace("  ", " ").replace("\n\n", "\n").replace("\n ", ", ").replace(" 0", ", 0").replace(" 1", ", 1")

def convertIndsToRST(basePath, M, K, Q):
    titlestr = "M = %d, K = %d, Q = %d" % (M, K, Q)
    filepat = basePath + "/inds/M=%d_K=%d_Q=%d_*.txt" % (M, K, Q)
    files = glob.glob(filepat)
    if len(files) == 0:
        print(filepat + " does not exist.")
        return

    fninds = files[0]

    # copy the original file to the build/html/
    bpath = basePath + "/../docs/build/html/db/M=%d/M=%d_K=%d_Q=%d.txt" % (M, M, K, Q)
    if not os.path.exists(os.path.dirname(bpath)):
        os.mkdir(os.path.dirname(bpath))
    if not os.path.exists(bpath) or (os.path.exists(bpath) and os.stat(bpath).st_mtime < os.stat(fninds).st_mtime):
        shutil.copyfile(fninds, bpath)
    
    mpath = basePath + "/../docs/source/db/M=%d/" % (M)
    if not os.path.exists(mpath):
        os.mkdir(mpath)

    fname = mpath + "M=%d_K=%d_Q=%d.rst" % (M, K, Q)
    
    if not os.path.exists(fname) or (os.path.exists(fname) and os.stat(fname).st_mtime < os.stat(fninds).st_mtime):
        with open(fname, mode = 'w') as f:
            f.write("\n")
            f.write("=" * len(titlestr) + "\n")
            f.write(titlestr + "\n")
            f.write("=" * len(titlestr) + "\n")
            f.write("\n")

            fn = os.path.basename(fninds)
            iurl = "https://github.com/imtoolkit/imtoolkit/blob/master/imtoolkit/inds/" + fn.replace("=", "%3D")
            f.write("`" + fn + " is available here. <" + iurl + ">`_\n\n")
            
            fn = fn.replace(".txt", "")
            p = Parameters(fn)
            if p.Q <= 1024:
                inds = np.loadtxt(fninds, dtype = np.int)
                inds = inds.reshape(p.Q, p.K).tolist()

                if p.Q <= 128:
                    at = np.array(convertIndsToMatrix(inds, M))
                    ats = numpyToPythonStr(str(at))
                    vrstr = numpyToPythonStr(str(np.array(convertIndsToVector(inds, M)).reshape(-1, p.M)))
                    vrstr = vrstr.replace("], ", "],\n     ")
            
            #ts = fn.replace("M=%d_"%M, "").replace("_minh=%d"%p["minh"], "").replace("_ineq=%d"%p["ineq"], "").replace("_", ", ").replace("=", " = ")
            #print(ts)
            #print("-" * len(ts))
            f.write(".. code-block:: python\n\n")
            f.write("    # minimum Hamming distance = %d\n" % p["minh"])
            f.write("    # activation inequality = %d\n" % p["ineq"])
            if p.Q <= 1024:
                f.write("    # active indices\n")
                f.write("    a = " + str(inds) + "\n")
                if p.Q <= 128:  
                    f.write("    # activation tensor\n")
                    f.write("    A = " + ats + "\n")
                    f.write("    # vector representation\n")
                    f.write("    " + vrstr + "\n")
                else:
                    f.write("    # activation tensor and its vector representation are omitted.\n")
            else:
                f.write("    # active indices, activation tensor and its vector representation are omitted.\n")
            
            f.write("\n")
            
        print("The generated rst was saved to " + fname)

def main():

    #print("DEBUG MODE ENABLED")
    #np.set_printoptions(threshold=np.inf)
    #basePath = os.path.dirname(os.path.abspath(__file__))
    #convertIndsToRST(basePath, 16, 5, 2)
    #quit()

    if len(sys.argv) <= 1:
        print("DECPARAMS_M=32")
        print("DECPARAMSDO_M=32")
        print("SEARCHPARAMS_M=32_P=2")
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
        print("DOCMUPDATE_M=32")
        print("DOCMINDEX")
        print("COVERAGE")
        quit()

    args = sys.argv[1:]
    for arg in args:
        print("-" * 50)
        print("arg = " + arg)
        params = Parameters(arg)
        basePath = os.path.dirname(os.path.abspath(__file__))

        start_time = time.time()
        if params.mode == "COVERAGE":
            allpossibleparams = 0
            hitcount = 0
            M = 2
            while True:
                for K in range(1, M):
                    ps = getIMParameters(M, K)
                    for p in ps:
                        allpossibleparams += 1
                        M, K, Q = p[0], p[1], p[2]
                        fpy = glob.glob(basePath + "/inds/M=%d_K=%d_Q=%d_*.txt" % (M, K, Q))
                        if len(fpy) > 0:
                            hitcount += 1
                M += 2
                print("M <= %d, %d / %d = %2.2f" % (M, hitcount, allpossibleparams, 100.0 * hitcount / allpossibleparams))
                if M == 32:
                    break

        elif params.mode == "SEARCHPARAMS" or params.mode == "SEARCHPARAMSDO":
            imparams = []
            allpossibleparams = 0
            M = 2
            while True:
                for K in range(1, M):
                    ps = getIMParameters(M, K)
                    for p in ps:
                        allpossibleparams += 1
                        M, K, Q = p[0], p[1], p[2]
                        fpy = glob.glob(basePath + "/inds/M=%d_K=%d_Q=%d_*.txt" % (M, K, Q))
                        if len(fpy) == 0:
                            imparams.append(p)

                        #else:
                        #    if Q == 2 or Q * K <= M:
                        #        print("May be wrong: /inds/M=%d_K=%d_Q=%d*.txt" % (M, K, Q))
                        #        os.remove(fpy[0])
                        #    fpy = glob.glob(basePath + "/decs/M=%d_K=%d.txt" % (M, K))
                        #    if (len(fpy)) == 0:
                        #        print("May be wrong: /inds/M=%d_K=%d_Q=%d*.txt" % (M, K, Q))
                M += 2
                if M > params.M:
                    break
            
            print("Possible IM parameters = %d" % allpossibleparams)
            print("Supported IM parameters = %d" % (allpossibleparams - len(imparams)))
            print("Search coverage = %.2f percent" % (100.0 - 100.0 * len(imparams) / allpossibleparams))
            imparams.sort(key = lambda x:x[2])
            cmds = []
            for p in imparams:
                cmd = "imsearch SEARCH_M=%d_K=%d_Q=%d" % (p[0], p[1], p[2])
                cmds.append(cmd)
            
            if params.mode == "SEARCHPARAMS":
                for p in range(params.P):
                    print("Set %d ====================================" % p)
                    i = 0
                    for cmd in cmds:
                        if i % params.P == p:
                            print(cmd)
                        i += 1
                    print("")
            elif params.mode == "SEARCHPARAMSDO":
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
            if params.Q == 2 or params.Q * params.K <= params.M:
                print("A self-evident solution is available for this setup.")
                #params = Parameters("M=26_K=25_Q=16")
                qstarts = np.floor(np.arange(params.Q) * (params.M - params.K) / (params.Q - 1) + 0.5)
                inds = np.zeros((params.Q, params.K), dtype = np.int)
                for q in range(params.Q):
                    inds[q] = qstarts[q] + np.arange(params.K)

                outputIndsToFile(inds, params.M)
            else:
                fname = outputCPLEXModelFile(params.M, params.K, params.Q)
                if fname != None and ".mod" in fname:
                    os.system("oplrun " + fname)
                    # Convert the obtained solution to a numpy file
                    fcout = glob.glob(basePath + "/inds-raw/M=%d_K=%d_Q=%d_*.txt" % (params.M, params.K, params.Q))
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
        elif params.mode == "DOCMUPDATE":
            np.set_printoptions(threshold=np.inf)
            M = 2
            while True:
                for K in range(1, M):
                    ps = getIMParameters(M, K)
                    for p in ps:
                        M, K, Q = p[0], p[1], p[2]
                        convertIndsToRST(basePath, M, K, Q)
                M += 2
                if M > params.M:
                    break
        elif params.mode == "DOCMINDEX":
            np.set_printoptions(threshold=np.inf)
            def lfs(f):
                fn = os.path.basename(f).replace(".rst", "")
                p = Parameters(fn)
                return (p.M * 32 + p.K) * 10000000 + p.Q
            
            dirs = glob.glob(basePath + "/../docs/source/db/M=*")

            for mdir in dirs:
                print(mdir)
                M = int(os.path.basename(mdir).replace("M=", ""))
                titlestr = "M = %d" % M

                files = glob.glob(mdir + "/M=*.rst")
                files.sort(key = lfs)

                fout = mdir + "/index.rst"
                with open(fout, mode = 'w') as f:
                    f.write("\n")
                    f.write("=" * len(titlestr) + "\n")
                    f.write(titlestr + "\n")
                    f.write("=" * len(titlestr) + "\n")
                    f.write("\n\n")
                    f.write("This webpage provides the designed active indices for the :math:`M = %d` case.\n\n" % M)

                    frsts = [os.path.basename(frst).replace(".rst", "") for frst in files]
                    f.write(".. toctree::\n")
                    f.write("   :maxdepth: 2\n")
                    f.write("   :hidden:\n")
                    f.write("   \n")
                    for frst in frsts:
                        f.write("   " + frst + "\n")
                    f.write("\n")
                    
                    for frst in frsts:
                        f.write("- :doc:`" + frst + "`\n")
                print("The index.rst file was saved to " + fout)

        elapsed_time = time.time() - start_time
        print ("Elapsed time = %.10f seconds" % (elapsed_time))

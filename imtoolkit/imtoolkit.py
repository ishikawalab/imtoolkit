# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import os
import re
import sys
import time
import numpy as np
from imtoolkit import IMTOOLKIT_VERSION, Parameters, SymbolCode, IMCode, OSTBCode, DiagonalUnitaryCode, ADSMCode, TASTCode, IdealRayleighChannel, IdealOFDMChannel, CoherentMLDSimulator, DifferentialMLDSimulator, SemiUnitaryDifferentialMLDSimulator, NonSquareDifferentialMLDSimulator, Basis, getMinimumEuclideanDistance, getInequalityL1, getMinimumHammingDistance, convertIndsToVector


def main():
    np.set_printoptions(threshold=np.inf)

    title = "    IMToolkit Version " + IMTOOLKIT_VERSION + "    "
    print("=" * len(title) + "\n" + title + "\n" + "=" * len(title))
    
    if os.getenv("USECUPY") == "1":
        print("CuPy-aided GPGPU acceleration is activated in your environment.")
        print("One can activate the NumPy counterpart by executing")
        print("> unset USECUPY")
    else:
        print("NumPy is used for all the calculations.")
        print("The use of CUDA and CuPy is strongly recommended.")
        print("One can activate it by executing")
        print("> export USECUPY=1")
    print("")
    
    if len(sys.argv) <= 1 or (len(sys.argv) == 2 and "-h" in sys.argv[1]):
        print("IMToolkit official website: https://ishikawa.cc/imtoolkit/")
        print("A detailed tutorial: https://ishikawa.cc/imtoolkit/tutorial.html")
        print("Fork me on GitHub: https://github.com/imtoolkit/imtoolkit")

        quit()
    
    args = sys.argv[1:]
    for arg in args:
        lentitle = len(arg) + 6
        print("-" * lentitle + "\narg = " + arg + "\n" + "-" * lentitle)

        params = Parameters(arg)

        # initialize a codebook, which also supports BLAST/OFDM by setting M = K
        meanPower = 1 # For the MIMO scenario, the mean power is normalized to 1
        if params.channel == "ofdm":
            # For the OFDM scenario, the mean power of symbol vectors is normalized to M
            meanPower = params.M

        if params.code == "symbol":
            code = SymbolCode(params.mod, params.L)
        elif params.code == "index":
            code = IMCode(params.dm, params.M, params.K, params.Q, params.mod, params.L, meanPower)
        elif params.code == "OSTBC":
            if params.isSpeficied("O"):
                code = OSTBCode(params.M, params.mod, params.L, params.O)
            else:
                code = OSTBCode(params.M, params.mod, params.L)
        elif params.code == "DUC":
            code = DiagonalUnitaryCode(params.M, params.L)
        elif params.code == "ADSM":
            code = ADSMCode(params.M, params.mod, params.L)
        elif params.code == "TAST":
            code = TASTCode(params.M, params.Q, params.L)
        
        # initialize a channel generator
        if params.channel == "rayleigh": # quasi-static Rayleigh fading
            if re.match(r'.*P$', params.mode):
                # Parallel channel
                channel = IdealRayleighChannel(params.ITi, params.M, params.N)
            else:
                # Single channel
                channel = IdealRayleighChannel(1, params.M, params.N)
        elif params.channel == "ofdm": # ideal frequency-selective OFDM channel
            params.N = params.M
            if re.match(r'.*P$', params.mode):
                # Parallel channel
                channel = IdealOFDMChannel(params.ITi, params.M)
            else:
                # Single channel
                channel = IdealOFDMChannel(1, params.M)

        # initialize a simulator
        if params.sim == "coh":
            sim = CoherentMLDSimulator(code.codes, channel)
        elif params.sim == "diff":
            sim = DifferentialMLDSimulator(code.codes, channel)
        elif params.sim == "sudiff":
            sim = SemiUnitaryDifferentialMLDSimulator(code.codes, channel)
        elif params.sim == "nsdiff":
            bases = Basis(params.basis, params.M, params.T).bases
            sim = NonSquareDifferentialMLDSimulator(code.codes, channel, bases)

        start_time = time.time()

        if params.mode == "RATE":
            code.putRate()
        elif params.mode == "MED":
            print("MED = " + str(getMinimumEuclideanDistance(code.codes)))
        elif params.mode == "BER":
            sim.simulateBERReference(params)
        elif params.mode == "BERP":
            sim.simulateBERParallel(params)
        elif params.mode == "AMI":
            sim.simulateAMIReference(params)
        elif params.mode == "AMIP":
            sim.simulateAMIParallel(params)
        elif params.mode == "VIEW":
            print(code.codes)
        elif params.mode == "VIEWIM":
            print(np.array(convertIndsToVector(code.inds, params.M)).reshape(-1, params.Q))
            print("Minimum Hamming distance = %d" % getMinimumHammingDistance(code.inds, params.M))
            print("Inequality L1 = %d" % getInequalityL1(code.inds, params.M))
        elif params.mode == "VIEWIMTEX":
            print("$\\a$(%d, %d, %d) $=$ [" % (params.M, params.K, params.Q))
            es = [", ".join(["%d" % (i+1) for i in iarr]) for iarr in code.inds]
            print(", ".join(["[" + e + "]" for e in es]) + "].")

        elapsed_time = time.time() - start_time
        print ("Elapsed time = %.10f seconds" % (elapsed_time))

if __name__ == '__main__':
    main()

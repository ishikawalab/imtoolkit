# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import re
import sys
import time
from imtoolkit import *


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
            if params.isSpeficied("u1"):
                code = ADSMCode(params.M, params.mod, params.L, params.u1)
            else:
                code = ADSMCode(params.M, params.mod, params.L)
        elif params.code == "TAST":
            code = TASTCode(params.M, params.Q, params.L, params.mod)
        
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
        elif params.channel == "rice": # ideal Rician fading
            # channel parameters, that need to be modified based on your setup
            print("bohagen2007los")
            frequency = 5.0 * 10**9 # 5 [GHz]
            wavelength = frequencyToWavelength(frequency)
            height = params.R if params.isSpeficied("R") else 3.0
            dTx = params.dTx if params.isSpeficied("dTx") else height / max(params.M, params.N)
            print("dTx = %1.2f"%dTx)
            rx, ry, rz = IdealRicianChannel.getPositionsUniformLinearArray(params.N, wavelength, 0)
            tx, ty, tz = IdealRicianChannel.getPositionsUniformLinearArray(params.M, dTx, height)
            #tx, ty, tz = IdealRicianChannel.getPositionsRectangular2d(params.M, wavelength, 3.0)
            #rx, ry, rz = IdealRicianChannel.getPositionsRectangular2d(params.N, wavelength, 0.0)

            if re.match(r'.*P$', params.mode):
                # Parallel channel
                channel = IdealRicianChannel(params.ITi, params.Kf, wavelength, tx, ty, tz, rx, ry, rz)
            else:
                # Single channel
                channel = IdealRicianChannel(1, params.Kf, wavelength, tx, ty, tz, rx, ry, rz)

        # initialize a simulator
        if params.sim == "coh":
            sim = CoherentMLDSimulator(code.codes, channel)
        elif params.sim == "diff":
            sim = DifferentialMLDSimulator(code.codes, channel)
        elif params.sim == "sudiff":
            sim = SemiUnitaryDifferentialMLDSimulator(code.codes, channel)
        elif params.sim == "nsdiff":
            E1 = Basis.getGSPE1(params) if params.basis[0] == "g" else None
            bases = Basis(params.basis, params.M, params.T, E1=E1).bases
            sim = NonSquareDifferentialMLDSimulator(code.codes, channel, bases)
        elif params.sim == "nsdiffc" or params.sim == "nsdiffce":
            E1 = Basis.getGSPE1(params) if params.basis[0] == "g" else None
            txbases = ChaosBasis(params.basis, params.M, params.T, params.W, params.x0, params.Ns, E1 = E1).bases
            if params.isSpeficied("d"):
                rxbases = ChaosBasis(params.basis, params.M, params.T, params.W, params.x0 + params.d, params.Ns, E1 = E1).bases
            else:
                rxbases = txbases
            sim = NonSquareDifferentialChaosMLDSimulator(code.codes, channel, txbases, rxbases)

        start_time = time.time()

        if params.mode == "RATE":
            code.putRate()
        elif params.mode == "MED":
            if params.sim == "nsdiff":
                print("MED = " + str(getMinimumEuclideanDistance(np.matmul(code.codes, bases[0]))))
            else:
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
            if params.sim == "nsdiff":
                print(np.matmul(code.codes, bases[0]))
            else:
                print(code.codes)
        elif params.mode == "VIEWIM":
            print(np.array(convertIndsToVector(code.inds, params.M)).reshape(-1, params.Q))
            print("Minimum Hamming distance = %d" % getMinimumHammingDistance(code.inds, params.M))
            print("Inequality L1 = %d" % getInequalityL1(code.inds, params.M))
        elif params.mode == "VIEWIMTEX":
            print("$\\a$(%d, %d, %d) $=$ [" % (params.M, params.K, params.Q))
            es = [", ".join(["%d" % (i+1) for i in iarr]) for iarr in code.inds]
            print(", ".join(["[" + e + "]" for e in es]) + "].")
        elif params.mode == "CONST":
            if params.sim == "nsdiffc":
                Nc = code.codes.shape[0]
                symbols = np.array([np.matmul(code.codes[i], txbases[:, :, 0]) for i in range(Nc)]).reshape(-1)
            elif params.sim == "nsdiff":
                symbols = np.matmul(code.codes, bases[0]).reshape(-1)
            else:
                symbols = code.codes.reshape(-1)
            df = {"real": np.real(symbols), "imag": np.imag(symbols)}
            Simulator.saveCSV(arg, df)
        elif params.mode == "SEARCH":
            if params.code == "TAST":
                TASTCode.search(params.M, params.Q, params.L)

        elapsed_time = time.time() - start_time
        print ("Elapsed time = %.10f seconds" % (elapsed_time))

if __name__ == '__main__':
    main()

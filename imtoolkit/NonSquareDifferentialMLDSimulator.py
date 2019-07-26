# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import os
from tqdm import tqdm, trange
if os.getenv("USECUPY") == "1":
    from cupy import *
else:
    from numpy import *

from .Simulator import Simulator
from .Util import getXORtoErrorBitsArray, inv_dB, randn_c

class NonSquareDifferentialMLDSimulator(Simulator):
    """A simulatror that relies on the nonsquare differential space-time block codes, which are proposed in [1-3]. This implementation uses the square-to-nonsquare projection concept of [2] and the adaptive forgetting factor of [3] for time-varying channels. The environment variable USECUPY determines whether to use cupy or not.

    [1] N. Ishikawa and S. Sugiura, ``Rectangular differential spatial modulation for open-loop noncoherent massive-MIMO downlink,'' IEEE Trans. Wirel. Commun., vol. 16, no. 3, pp. 1908–1920, 2017.

    [2] N. Ishikawa, R. Rajashekar, C. Xu, S. Sugiura, and L. Hanzo, ``Differential space-time coding dispensing with channel-estimation approaches the performance of its coherent counterpart in the open-loop massive MIMO-OFDM downlink,'' IEEE Trans. Commun., vol. 66, no. 12, pp. 6190–6204, 2018.

    [3] N. Ishikawa, R. Rajashekar, C. Xu, M. El-Hajjar, S. Sugiura, L. L. Yang, and L. Hanzo, ``Differential-detection aided large-scale generalized spatial modulation is capable of operating in high-mobility millimeter-wave channels,'' IEEE J. Sel. Top. Signal Process., in press.

    Args:
        codes (ndarray): an input codebook, which is generated on the CPU memory and is transferred into the GPU memory.
        channel (imtoolkit.Channel): a channel model used in simulation.
    """

    def __init__(self, codes, channel, bases):
        super().__init__(codes, channel)
        self.bases = bases

    def simulateBERReference(self, params, outputFile = True, printValue = True):
        """Simulates BER values at multiple SNRs, where the straightforward reference algorithm is used. Note that this time complexity is unrealistically high. 

        Args:
            params (imtoolkit.Parameter): simulation parameters.
            outputFile (bool): a flag that determines whether to output the obtained results to the results/ directory.
            printValue (bool): a flag that determines whether to print the simulated values.

        Returns:
            ret (dict): a dict that has two keys: snr_dB and ber, and contains the corresponding results. All the results are transferred into the CPU memory.
        """

        IT, M, N, T, W, Nc, B, codes, bases = params.IT, params.M, params.N, params.T, params.W, self.Nc, self.B, self.codes, self.bases
        snr_dBs = linspace(params.snrfrom, params.to, params.len)
        sigmav2s = 1.0 / inv_dB(snr_dBs)
        xor2ebits = getXORtoErrorBitsArray(Nc)
        E1 = bases[0] # M \times T
        E1H = E1.T.conj()
        Xrs = matmul(codes, E1) # Nc \times M \times T

        bers = zeros(len(snr_dBs))
        for i in trange(len(snr_dBs)):
            errorBits = 0
            
            for it in range(IT):
                S0 = eye(M, dtype = complex)
                Yhat0 = Yhat1 = zeros((N, M), dtype = complex)

                self.channel.randomize()
                H = self.channel.getChannel() # N \times M

                for wi in range(1, int(W / T) + 1):
                    if wi <= M / T:
                        S1 = eye(M, dtype=complex)
                        Sr1 = bases[wi - 1]
                        X1 = S1
                        Y1 = matmul(H, Sr1) + randn_c(N, T) * sqrt(sigmav2s[i]) # N \times T
                        Yhat1 += matmul(Y1, bases[wi - 1].T.conj())
                    else:
                        codei = random.randint(0, Nc)
                        X1 = codes[codei]
                        S1 = matmul(S0, X1)
                        Sr1 = matmul(S1, E1)
                        Y1 = matmul(H, Sr1) + randn_c(N, T) * sqrt(sigmav2s[i]) # N \times T

                        # estimate
                        p = power(abs(Y1 - matmul(Yhat0, Xrs)), 2) # Nc \times N \times M
                        norms = sum(p, axis = (1,2)) # summation over the (N,M) axes
                        mini = argmin(norms)
                        Xhat1 = codes[mini]

                        # adaptive forgetting factor
                        Yhd = matmul(Yhat0, Xhat1)
                        D1 = Y1 - matmul(Yhd, E1)
                        n1 = power(linalg.norm(D1), 2)
                        estimatedAlpha = N * T * sigmav2s[i] / n1
                        estimatedAlpha = min(max(estimatedAlpha, 0.01), 0.99)
                        Yhat1 = (1.0 - estimatedAlpha) * matmul(D1, E1H) + Yhd

                        errorBits += sum(xor2ebits[codei ^ mini])

                    X0 = X1
                    S0 = S1
                    Y0 = Y1
                    Yhat0 = Yhat1

            bers[i] = errorBits / (IT * B * (W - M)) * T
            
            if printValue:
                print("At SNR = %1.2f dB, BER = %d / %d = %1.20e" % (snr_dBs[i], errorBits, (IT * B * (W - M)) / T, bers[i]))

        ret = self.dicToNumpy({"snr_dB": snr_dBs, "ber": bers})
        if outputFile:
            self.saveCSV(params.arg, ret)
            print(ret)
        return ret

    def simulateBERParallel(self, params, outputFile = True, printValue = True):
        """Simulates BER values at multiple SNRs, where the massively parallel algorithm is used. This implementation is especially designed for cupy.

        Args:
            params (imtoolkit.Parameter): simulation parameters.
            outputFile (bool): a flag that determines whether to output the obtained results to the results/ directory.
            printValue (bool): a flag that determines whether to print the simulated values.

        Returns:
            ret (dict): a dict that has two keys: snr_dB and ber, and contains the corresponding results. All the results are transferred into the CPU memory.
        """

        ITo, ITi, M, N, T, W, Nc, B, codes = params.ITo, params.ITi, params.M, params.N, params.T, params.W, self.Nc, self.B, self.codes
        bases = asarray(self.bases)

        if Nc > ITi:
            print("ITi should be larger than Nc = %d." % Nc)

        snr_dBs = linspace(params.snrfrom, params.to, params.len)
        lsnr = len(snr_dBs)
        sigmav2s = 1.0 / inv_dB(snr_dBs)
        sqrtsigmav2s = repeat(sqrt(sigmav2s), ITi * N * T).reshape(lsnr, ITi, N, T)
        xor2ebits = getXORtoErrorBitsArray(Nc)
        eyes = tile(eye(M, dtype=complex), lsnr * ITi).T.reshape(lsnr, ITi, M, M) # lsnr \times ITi \times M \times M
        E1 = bases[0] # M \times T
        E1H = E1.T.conj()
        Xrs = matmul(codes, E1) # Nc \times M \times T
        Xrsmat = hstack(Xrs) # M \times T * Nc

        indspermute = random.permutation(arange(ITi))
        codei = tile(arange(Nc), int(ceil(ITi / Nc)))[0:ITi]
        X1 = take(codes, codei, axis=0) # ITi \times M \times M
        
        bers = zeros(lsnr)
        for ito in trange(ITo):
            self.channel.randomize()
            Ho = self.channel.getChannel().reshape(ITi, N, M) # ITi \times N \times M
            # The followings are very slow
            #H = asarray(split(tile(Ho, lsnr), lsnr, axis=2)) # lsnr \times ITi \times N \times M
            #H = rollaxis(repeat(Ho, lsnr, axis=0).reshape(ITi, lsnr, N, M), 1) # lsnr \times ITi \times N \times M
            # This simple for loop is the fastest
            H = zeros((lsnr, ITi, N, M), dtype=complex)
            for i in range(lsnr):
                H[i] = Ho

            S0 = eyes[0] # ITi \times M \times M
            Yhat0 = Yhat1 = zeros((lsnr, ITi, N, M), dtype = complex) # lsnr \times ITi \times N \times M

            for wi in range(1, int(W / T) + 1):
                Vo = randn_c(ITi, N, T) # ITi \times N \times T
                V1 = zeros((lsnr, ITi, N, T), dtype=complex)
                for i in range(lsnr):
                    V1[i] = sqrt(sigmav2s[i]) * Vo

                if wi <= M / T:
                    S1 = eyes[0]
                    Y1 = matmul(H, bases[wi - 1]) + V1 # lsnr \tiems ITi \times N \times T
                    Yhat1 += matmul(Y1, bases[wi - 1].T.conj()) # lsnr \tiems ITi \times N \times M
                else:
                    codei = codei[indspermute]
                    X1 = X1[indspermute] # ITi \times M \times M
                    S1 = matmul(S0, X1) # ITi \times M \times M
                    Sr1 = matmul(S1, E1) # ITi \times M \times T
                    Y1 = matmul(H, Sr1) + V1 # lsnr \times ITi \times N \times T

                    # estimate
                    YhXrs = matmul(Yhat0, Xrsmat) # lsnr \times ITi \times N \times T * Nc
                    ydifffro = power(abs(Y1 - YhXrs), 2).reshape(lsnr, ITi, N, Nc, T)
                    norms = sum(ydifffro, axis=(2, 4)) # lsnr \times ITi \times Nc
                    mini = argmin(norms, axis=2) # lsnr \times ITi
                    Xhat1 = codes[mini]  # lsnr \times ITI \times M \time M

                    # adaptive forgetting factor
                    Yhd = matmul(Yhat0, Xhat1)  # lsnr \times ITi \times N \times M
                    D1 = Y1 - matmul(Yhd, E1)  # lsnr \times ITi \times N \times T
                    n1 = sum(power(abs(D1), 2), axis=(2, 3))  # lsnr \times ITi

                    elphas = N * T * matmul(diag(sigmav2s), 1.0 / n1)  # lsnr \times ITi estimated alpha coefficients
                    elphas[where(elphas < 0.01)] = 0.01
                    elphas[where(elphas > 0.99)] = 0.99

                    elphastensor = repeat(1 - elphas, N * M).reshape(lsnr, ITi, N, M)
                    Yhat1 = elphastensor * matmul(D1, E1H) + Yhd  # lsnr \times ITi \times N \times M
                    bers += sum(xor2ebits[codei ^ mini], axis = 1) # lsnr

                S0 = S1
                Yhat0 = Yhat1

            if printValue:
                nbits = (ito + 1) * ITi * B * (W - M) / T
                for i in range(lsnr):
                    print("At SNR = %1.2f dB, BER = %d / %d = %1.10e" % (
                    snr_dBs[i], bers[i], nbits, bers[i] / nbits))
                
            
        bers = bers / (ITo * ITi * B * (W - M)) * T
        ret = self.dicToNumpy({"snr_dB": snr_dBs, "ber": bers})
        if outputFile:
            self.saveCSV(params.arg, ret)
            print(ret)
        return ret


# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import os
import sys
import itertools
from tqdm import tqdm, trange
import importlib
if os.getenv("USECUPY") == "1" and importlib.util.find_spec("cupy") != None:
    from cupy import *
    # print("cupy is imported by CoherentMLDSimulator.py")
else:
    from numpy import *
    # print("numpy is imported by CoherentMLDSimulator.py")

from .Simulator import *
from .Util import *

class CoherentMLDSimulator(Simulator):
    """A simulatror that relies on the coherent maximum likelihood detection.

    Args:
        codes (ndarray): an input codebook
        channel (imtoolkit.Channel): a channel model used though simulation
    """

    def __init__(self, codes, channel):
        super().__init__(codes, channel)

    def simulateBERReference(self, params, output = True):
        """Simulates the BER values at multiple SNRs, where the straightforward reference algorithm is used.

        Args:
            params (imtoolkit.Parameter): simulation parameters.
            output (bool): whether output the obtained results to the results/ directory.

        Returns:
            ret (dict): a dict that has two keys: snr_dB and ber, and the corresponding results.
        """

        IT, M, N, Nc, B, codes = params.IT, params.M, params.N, self.Nc, self.B, self.codes
        snr_dBs = linspace(params.snrfrom, params.to, params.len)
        sigmav2s = 1.0 / inv_dB(snr_dBs)
        errorTable = getErrorBitsTable(Nc)

        bers = zeros(len(snr_dBs))
        for i in trange(len(snr_dBs)):
            errorBits = 0
            for it in range(IT):
                codei = random.randint(0, Nc)
                self.channel.randomize()
                h = self.channel.getChannel() # N \times M
                v = randn_c(N, 1) * sqrt(sigmav2s[i])
                y = matmul(h, codes[codei]) + v

                norms = sum(power(abs(y - matmul(h, codes)), 2), axis = 1)
                mini = argmin(norms)
                errorBits += errorTable[codei][mini]

            bers[i] = errorBits / (IT * B)
            print("At SNR = %1.2f dB, BER = %d / %d = %1.20f" % (snr_dBs[i], errorBits, IT * B, bers[i]))

        ret = {"snr_dB": snr_dBs, "ber": bers}
        if output:
            self.saveCSV(params.arg, self.dicToDF(ret))
            print(ret)
        return ret

    def simulateBERParallel(self, params, output = True):
        """Simulates the BER values at multiple SNRs, where the massively parallel algorithm is used.

        Args:
            params (imtoolkit.Parameter): simulation parameters.
            output (bool): whether output the obtained results to the results/ directory.

        Returns:
            ret (dict): a dict that has two keys: snr_dB and ber, and the corresponding results.
        """
        print("simulateBERParallel")

        M, N, ITo, ITi, Nc, B, codes = params.M, params.N, params.ITo, params.ITi, self.Nc, self.B, self.codes
        snr_dBs = linspace(params.snrfrom, params.to, params.len)
        sigmav2s = 1.0 / inv_dB(snr_dBs)
        codei = tile(arange(Nc), ITi)
        xor2ebits = getXORtoErrorBitsArray(Nc)

        x = tile(codes, Nc) # Nc \times M \times T \cdot Nc
        y = x.T # Nc \times M \times T \cdot Nc
        print(y.shape)
        diffxy = hstack(x-y) # M \times Nc * Nc

        bers = zeros(len(snr_dBs))
        for ito in trange(ITo):
            self.channel.randomize()
            bigh = self.channel.getChannel() # ITi * N \times M
            bigv = tile(randn_c(ITi * N).reshape(-1, 1), Nc * Nc) # ITi * N \times Nc * Nc

            for i in range(len(snr_dBs)):
                ydiff = matmul(bigh, diffxy) + bigv * sqrt(sigmav2s[i])

                ydifffro = power(abs(ydiff.reshape(ITi, N, Nc * Nc)), 2) # ITi \times N \times Nc * Nc
                ydifffrosum = sum(ydifffro, axis = 1) # ITi \times Nc * Nc
                norms = ydifffrosum.reshape(ITi, Nc, Nc) # ITi \times Nc \times Nc
                # print(norms)
                mini = argmin(norms, axis = 2).reshape(ITi * Nc)
                errorBits = sum(xor2ebits[bitwise_xor(codei, mini)])

                bers[i] += errorBits# / (ITi * B * Nc)
                nbits = (ito + 1) * ITi * B * Nc
                print("At SNR = %1.2f dB, BER = %d / %d = %1.20f" % (snr_dBs[i], bers[i], nbits, bers[i] / nbits))

        bers /= ITo * ITi * B * Nc
        ret = {"snr_dB": snr_dBs, "ber": bers}
        if output:
            self.saveCSV(params.arg, self.dicToDF(ret))
            print(ret)
        return ret


    def simulateAMIReference(self, params, output = True):
        """Simulates the AMI values at multiple SNRs, where the straightforward reference algorithm is used.

        Args:
            params (imtoolkit.Parameter): simulation parameters.
            output (bool): whether output the obtained results to the results/ directory.

        Returns:
            ret (dict): a dict that has two keys: snr_dB and ami, and the corresponding results.
        """
        print("simulateAMIReference")

        IT, M, N, Nc, B, codes = params.IT, params.M, params.N, self.Nc, self.B, self.codes
        snr_dBs = linspace(params.snrfrom, params.to, params.len)
        sigmav2s = 1.0 / inv_dB(snr_dBs)

        amis = zeros(len(snr_dBs))
        for i in trange(len(snr_dBs)):
            sum_outer = 0.0
            for it in range(IT):
                V = sqrt(sigmav2s[i]) * randn_c(N, 1)
                #V = sqrt(sigmav2) * seedv.reshape(M, 1) # for debug
                self.channel.randomize()
                H = self.channel.getChannel() # N \times M
                # H = eye(M) # for debug
                for outer in range(Nc):
                    sum_inner = 0.0
                    for inner in range(Nc):
                        hxy = matmul(H, codes[outer] - codes[inner])
                        head = hxy + V
                        tail = V
                        coeff = (-power(linalg.norm(head), 2) + power(linalg.norm(tail), 2)) / sigmav2s[i]
                        sum_inner += exp(coeff)
                    sum_outer += log2(sum_inner)
            #print("bminus = " + str(sum_outer / Nc / IT))
            amis[i] = B - sum_outer / Nc / IT
            if output:
                print("At SNR = %1.2f dB, AMI = %1.20f" % (snr_dBs[i], amis[i]))

        ret = {"snr_dB": snr_dBs, "ami": amis}
        if output:
            print(ret)
            self.saveCSV(params.arg, ret)
        return ret
        

    def simulateAMIParallel(self, params, output = True):
        """Simulates the AMI values at multiple SNRs, where the massively parallel algorithm is used.

        Args:
            params (imtoolkit.Parameter): simulation parameters.
            output (bool): whether output the obtained results to the results/ directory.

        Returns:
            ret (dict): a dict that has two keys: snr_dB and ami, and the corresponding results.
        """
        M, N, ITo, ITi, Nc, B, codes = params.M, params.N, params.ITo, params.ITi, self.Nc, self.B, self.codes
        snr_dBs = linspace(params.snrfrom, params.to, params.len)
        sigmav2s = 1.0 / inv_dB(snr_dBs)

        x = tile(codes, Nc)
        y = x.T
        diffxy = hstack(x-y) # M \times Nc * Nc

        amis = zeros(len(snr_dBs))
        for ito in trange(ITo):
            self.channel.randomize()
            bigh = self.channel.getChannel() # ITi * N \times M
            bigv = tile(randn_c(ITi * N).reshape(-1, 1), Nc * Nc) # ITi * N \times Nc * Nc

            bigvfro = power(abs(bigv), 2).reshape(ITi, N, Nc * Nc) # ITi \times N \times Nc * Nc
            frov = sum(bigvfro, axis = 1).reshape(ITi, Nc, Nc)  # ITi \times Nc \times Nc
            
            for i in range(len(snr_dBs)):
                hsplusv = matmul(bigh, diffxy) + bigv * sqrt(sigmav2s[i]) # ITi * N \times Nc * Nc
                hsvfro = power(abs(hsplusv), 2).reshape(ITi, N, Nc * Nc) # ITi \times N \times Nc * Nc
                froy = sum(hsvfro, axis = 1) # ITi \times Nc * Nc
                reds = froy.reshape(ITi, Nc, Nc) # ITi \times Nc \times Nc

                ecoffs = -reds / sigmav2s[i] + frov # diagonal elements must be zero
                bminus = mean(log2(sum(exp(ecoffs), axis = 2)))

                amis[i] += B - bminus
                print("At SNR = %1.2f dB, AMI = %1.20f" % (snr_dBs[i], amis[i] / (ito + 1)))
            
        #
        ret = self.dicToNumpy({"snr_dB": snr_dBs, "ami": amis})
        if output:
            print(ret)
            self.saveCSV(params.arg, ret)

        return ret
        

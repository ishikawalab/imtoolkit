# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import os
from tqdm import tqdm, trange
if os.getenv("USECUPY") == "1":
    from cupy import *
    # print("cupy is imported by CoherentMLDSimulator.py")
else:
    from numpy import *
    # print("numpy is imported by CoherentMLDSimulator.py")

from .Simulator import *
from .Util import *

class CoherentMLDSimulator(Simulator):
    """A simulatror that relies on the coherent maximum likelihood detector, that assumes perfect channel state information at the receiver. The environment variable USECUPY determines whether to use cupy or not.

    Args:
        codes (ndarray): an input codebook, which is generated on the CPU memory and is transferred into the GPU memory.
        channel (imtoolkit.Channel): a channel model used in simulation.
    """

    def __init__(self, codes, channel):
        super().__init__(codes, channel)

    def simulateBERReference(self, params, outputFile = True, printValue = True):
        """Simulates BER values at multiple SNRs, where the straightforward reference algorithm is used. Note that this time complexity is unrealistically high. 

        Args:
            params (imtoolkit.Parameter): simulation parameters.
            outputFile (bool): a flag that determines whether to output the obtained results to the results/ directory.
            printValue (bool): a flag that determines whether to print the simulated values.

        Returns:
            ret (dict): a dict that has two keys: snr_dB and ber, and contains the corresponding results. All the results are transferred into the CPU memory.
        """

        IT, M, N, T, Nc, B, codes = params.IT, params.M, params.N, params.T, self.Nc, self.B, self.codes
        snr_dBs = linspace(params.snrfrom, params.to, params.len)
        sigmav2s = 1.0 / inv_dB(snr_dBs)
        xor2ebits = getXORtoErrorBitsArray(Nc)

        bers = zeros(len(snr_dBs))
        for i in trange(len(snr_dBs)):
            errorBits = 0
            for it in range(IT):
                codei = random.randint(0, Nc)
                self.channel.randomize()
                h = self.channel.getChannel() # N \times M
                v = randn_c(N, T) * sqrt(sigmav2s[i]) # N \times T
                y = matmul(h, codes[codei]) + v # N \times T

                p = power(abs(y - matmul(h, codes)), 2) # Nc \times N \times T
                norms = sum(p, axis = (1,2)) # summation over the (N,T) axes
                mini = argmin(norms)
                errorBits += sum(xor2ebits[codei ^ mini])

            bers[i] = errorBits / (IT * B)
            if printValue:
                print("At SNR = %1.2f dB, BER = %d / %d = %1.20f" % (snr_dBs[i], errorBits, IT * B, bers[i]))

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

        M, N, T, ITo, ITi, Nc, B, codes = params.M, params.N, params.T, params.ITo, params.ITi, self.Nc, self.B, self.codes
        snr_dBs = linspace(params.snrfrom, params.to, params.len)
        sigmav2s = 1.0 / inv_dB(snr_dBs)
        codei = tile(arange(Nc), ITi)
        xor2ebits = getXORtoErrorBitsArray(Nc)

        # The followings are old implementation proposed in [ishikawa2019im], which only support the T=1 case
        # x = tile(codes, Nc) # Nc \times M \times T * Nc
        # y = x.T # Nc \times M \times T * Nc
        # diffxy = hstack(x-y) # M \times Nc * Nc

        x = hstack(tile(codes, Nc)) # M \times T * Nc^2
        # x = [codes[0] codes[0] ... codes[0] codes[1] ...]
        y = tile(hstack(codes), Nc) # M \times T * Nc^2
        # y = [codes[0] codes[1] ... codes[Nc-1] codes[0] ...]
        diffxy = x - y # M \times T * Nc^2

        bers = zeros(len(snr_dBs))
        for ito in trange(ITo):
            self.channel.randomize()
            bigh = self.channel.getChannel() # ITi * N \times M
            bigv = tile(randn_c(ITi * N * T).reshape(-1, T), Nc * Nc) # ITi * N \times T * Nc^2

            for i in range(len(snr_dBs)):
                ydiff = matmul(bigh, diffxy) + bigv * sqrt(sigmav2s[i])  # ITi * N \times T * Nc^2

                # The followings are old implementation of [ishikawa2019im]
                # ydifffro = power(abs(ydiff.reshape(ITi, N, T * Nc * Nc)), 2) # ITi \times N \times T * Nc * Nc
                # ydifffrosum = sum(ydifffro, axis = 1) # ITi \times T * Nc * Nc
                
                ydifffro = power(abs(ydiff), 2).reshape(ITi, N, Nc * Nc, T) # ITi \times N \times Nc * Nc \times T
                ydifffrosum = sum(ydifffro, axis = (1,3)) # ITi \times Nc * Nc
                
                norms = ydifffrosum.reshape(ITi, Nc, Nc) # ITi \times Nc \times Nc
                # print(norms)
                mini = argmin(norms, axis = 2).reshape(ITi * Nc)
                errorBits = sum(xor2ebits[codei ^ mini])

                bers[i] += errorBits
                nbits = (ito + 1) * ITi * B * Nc
                if printValue:
                    print("At SNR = %1.2f dB, BER = %d / %d = %1.20f" % (snr_dBs[i], bers[i], nbits, bers[i] / nbits))

        bers /= ITo * ITi * B * Nc
        ret = self.dicToNumpy({"snr_dB": snr_dBs, "ber": bers})
        if outputFile:
            self.saveCSV(params.arg, ret)
            print(ret)
        return ret


    def simulateAMIReference(self, params, outputFile = True, printValue = True):
        """Simulates AMI values at multiple SNRs, where the straightforward reference algorithm is used. Note that this time complexity is unrealistically high. 

        Args:
            params (imtoolkit.Parameter): simulation parameters.
            outputFile (bool): a flag that determines whether to output the obtained results to the results/ directory.
            printValue (bool): a flag that determines whether to print the simulated values.

        Returns:
            ret (dict): a dict that has two keys: snr_dB and ber, and contains the corresponding results. All the results are transferred into the CPU memory.
        """

        IT, M, N, T, Nc, B, codes = params.IT, params.M, params.N, params.T, self.Nc, self.B, self.codes
        snr_dBs = linspace(params.snrfrom, params.to, params.len)
        sigmav2s = 1.0 / inv_dB(snr_dBs)

        amis = zeros(len(snr_dBs))
        for i in trange(len(snr_dBs)):
            sum_outer = 0.0
            for it in range(IT):
                V = sqrt(sigmav2s[i]) * randn_c(N, T)
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
            amis[i] = (B - sum_outer / Nc / IT) / T
            if printValue:
                print("At SNR = %1.2f dB, AMI = %1.20f" % (snr_dBs[i], amis[i]))

        ret = self.dicToNumpy({"snr_dB": snr_dBs, "ami": amis})
        if outputFile:
            print(ret)
            self.saveCSV(params.arg, ret)
        return ret
        

    def simulateAMIParallel(self, params, outputFile = True, printValue = True):
        """Simulates AMI values at multiple SNRs, where the massively parallel algorithm is used. This implementation is especially designed for cupy.

        Args:
            params (imtoolkit.Parameter): simulation parameters.
            outputFile (bool): a flag that determines whether to output the obtained results to the results/ directory.
            printValue (bool): a flag that determines whether to print the simulated values.

        Returns:
            ret (dict): a dict that has two keys: snr_dB and ber, and contains the corresponding results. All the results are transferred into the CPU memory.
        """
        
        M, N, T, ITo, ITi, Nc, B, codes = params.M, params.N, params.T, params.ITo, params.ITi, self.Nc, self.B, self.codes
        snr_dBs = linspace(params.snrfrom, params.to, params.len)
        sigmav2s = 1.0 / inv_dB(snr_dBs)

        # The following three variables are the same as those used in simulateBERParallel
        x = hstack(tile(codes, Nc)) # M \times T * Nc^2
        y = tile(hstack(codes), Nc) # M \times T * Nc^2
        diffxy = x - y # M \times T * Nc^2

        amis = zeros(len(snr_dBs))
        for ito in trange(ITo):
            self.channel.randomize()
            bigh = self.channel.getChannel() # ITi * N \times M
            bigv = tile(randn_c(ITi * N * T).reshape(-1, T), Nc * Nc) # ITi * N \times T * Nc^2

            bigvfro = power(abs(bigv), 2).reshape(ITi, N, Nc * Nc, T) # ITi \times N \times Nc^2 \times T
            frov = sum(bigvfro, axis = (1,3)).reshape(ITi, Nc, Nc)  # ITi \times Nc \times Nc
            
            for i in range(len(snr_dBs)):
                hsplusv = matmul(bigh, diffxy) + bigv * sqrt(sigmav2s[i]) # ITi * N \times T * Nc^2
                hsvfro = power(abs(hsplusv), 2).reshape(ITi, N, Nc * Nc, T) # ITi \times N \times Nc^2 \times T
                froy = sum(hsvfro, axis = (1,3)) # ITi \times Nc^2
                reds = froy.reshape(ITi, Nc, Nc) # ITi \times Nc \times Nc

                ecoffs = -reds / sigmav2s[i] + frov # diagonal elements must be zero
                bminus = mean(log2(sum(exp(ecoffs), axis = 2)))

                amis[i] += (B - bminus) / T
                if printValue:
                    print("At SNR = %1.2f dB, AMI = %1.20f" % (snr_dBs[i], amis[i] / (ito + 1)))
            
        #
        amis /= ITo
        ret = self.dicToNumpy({"snr_dB": snr_dBs, "ami": amis})
        if outputFile:
            print(ret)
            self.saveCSV(params.arg, ret)

        return ret
        

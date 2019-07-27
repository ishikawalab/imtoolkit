# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import os
from tqdm import trange

if os.getenv("USECUPY") == "1":
    from cupy import *
else:
    from numpy import *

from .Simulator import Simulator
from .Util import getXORtoErrorBitsArray, inv_dB, randn_c


class CoherentMLDSimulator(Simulator):
    """A simulator that relies on the coherent maximum likelihood detector, that assumes perfect channel state information at the receiver. The environment variable USECUPY determines whether to use cupy or not."""

    def __init__(self, codes, channel):
        """
        Args:
            codes (ndarray): an input codebook, which is generated on the CPU memory and is transferred into the GPU memory.
            channel (imtoolkit.Channel): a channel model used in simulation.
        """
        super().__init__(codes, channel)

    def simulateBERReference(self, params, outputFile=True, printValue=True):
        """Simulates BER values at multiple SNRs, where the straightforward reference algorithm is used. Note that this time complexity is unrealistically high. 

        Args:
            params (imtoolkit.Parameter): simulation parameters.
            outputFile (bool): a flag that determines whether to output the obtained results to the results/ directory.
            printValue (bool): a flag that determines whether to print the simulated values.

        Returns:
            dict: a dict that has two keys: snr_dB and ber, and contains the corresponding results. All the results are transferred into the CPU memory.
        """

        IT, N, T, Nc, B, codes = params.IT, params.N, params.T, self.Nc, self.B, self.codes
        snr_dBs = linspace(params.snrfrom, params.to, params.len)
        sigmav2s = 1.0 / inv_dB(snr_dBs)
        xor2ebits = getXORtoErrorBitsArray(Nc)

        bers = zeros(len(snr_dBs))
        for i in trange(len(snr_dBs)):
            errorBits = 0
            for _ in range(IT):
                codei = random.randint(0, Nc)
                self.channel.randomize()
                h = self.channel.getChannel()  # N \times M
                v = randn_c(N, T) * sqrt(sigmav2s[i])  # N \times T
                y = matmul(h, codes[codei]) + v  # N \times T

                p = power(abs(y - matmul(h, codes)), 2)  # Nc \times N \times T
                norms = sum(p, axis=(1, 2))  # summation over the (N,T) axes
                mini = argmin(norms)
                errorBits += sum(xor2ebits[codei ^ mini])

            bers[i] = errorBits / (IT * B)
            if printValue:
                print("At SNR = %1.2f dB, BER = %d / %d = %1.10e" % (snr_dBs[i], errorBits, IT * B, bers[i]))

        ret = self.dicToNumpy({"snr_dB": snr_dBs, "ber": bers})
        if outputFile:
            self.saveCSV(params.arg, ret)
            print(ret)
        return ret

    def simulateBERParallel(self, params, outputFile=True, printValue=True):
        """Simulates BER values at multiple SNRs, where the massively parallel algorithm is used. This implementation is especially designed for cupy.

        Args:
            params (imtoolkit.Parameter): simulation parameters.
            outputFile (bool): a flag that determines whether to output the obtained results to the results/ directory.
            printValue (bool): a flag that determines whether to print the simulated values.

        Returns:
            dict: a dict that has two keys: snr_dB and ber, and contains the corresponding results. All the results are transferred into the CPU memory.
        """

        M, N, T, ITo, ITi, Nc, B, codes = params.M, params.N, params.T, params.ITo, params.ITi, self.Nc, self.B, self.codes
        snr_dBs = linspace(params.snrfrom, params.to, params.len)
        lsnr = len(snr_dBs)
        sigmav2s = 1.0 / inv_dB(snr_dBs)
        codei = tile(arange(Nc), ITi)
        xor2ebits = getXORtoErrorBitsArray(Nc)

        # The followings are old implementation proposed in [ishikawa2019im], which only support the T=1 case
        # x = tile(codes, Nc) # Nc \times M \times T * Nc
        # y = x.T # Nc \times M \times T * Nc
        # diffxy = hstack(x-y) # M \times Nc * Nc

        x = hstack(tile(codes, Nc))  # M \times T * Nc^2
        # x = [codes[0] codes[0] ... codes[0] codes[1] ...]
        y = tile(hstack(codes), Nc)  # M \times T * Nc^2
        # y = [codes[0] codes[1] ... codes[Nc-1] codes[0] ...]
        diffxy = x - y  # M \times T * Nc^2

        bers = zeros(len(snr_dBs))
        for ito in trange(ITo):
            self.channel.randomize()
            Ho = self.channel.getChannel().reshape(ITi, N, M)  # ITi \times N \times M
            Vo = randn_c(ITi, N, T)  # ITi \times N \times T
            bigh = zeros((lsnr, ITi, N, M), dtype=complex)  # lsnr \times ITi \times N \times M
            bigv = zeros((lsnr, ITi, N, T), dtype=complex)  # lsnr \times ITi \times N \times T
            for i in range(lsnr):
                bigh[i] = Ho
                bigv[i] = sqrt(sigmav2s[i]) * Vo

            ydiff = matmul(bigh, diffxy) + bigv  # lsnr \times ITi \times N \times T * Nc^2
            ydifffro = power(abs(ydiff), 2).reshape(lsnr, ITi, N, Nc * Nc,
                                                    T)  # lsnr \times ITi \times N \times Nc * Nc \times T
            ydifffrosum = sum(ydifffro, axis=(2, 4))  # lsnr \times ITi \times Nc * Nc
            norms = ydifffrosum.reshape(lsnr, ITi, Nc, Nc)  # lsnr \times ITi \times Nc \times Nc
            mini = argmin(norms, axis=3).reshape(lsnr, ITi * Nc)  # lsnr \times ITi * Nc
            bers += sum(xor2ebits[codei ^ mini], axis=1)

            if printValue:
                nbits = (ito + 1) * ITi * B * Nc
                for i in range(lsnr):
                    print("At SNR = %1.2f dB, BER = %d / %d = %1.10e" % (snr_dBs[i], bers[i], nbits, bers[i] / nbits))

        bers /= ITo * ITi * B * Nc
        ret = self.dicToNumpy({"snr_dB": snr_dBs, "ber": bers})
        if outputFile:
            self.saveCSV(params.arg, ret)
            print(ret)
        return ret

    def simulateAMIReference(self, params, outputFile=True, printValue=True):
        """Simulates AMI values at multiple SNRs, where the straightforward reference algorithm is used. Note that this time complexity is unrealistically high. 

        Args:
            params (imtoolkit.Parameter): simulation parameters.
            outputFile (bool): a flag that determines whether to output the obtained results to the results/ directory.
            printValue (bool): a flag that determines whether to print the simulated values.

        Returns:
            dict: a dict that has two keys: snr_dB and ami, and contains the corresponding results. All the results are transferred into the CPU memory.
        """

        IT, N, T, Nc, B, codes = params.IT, params.N, params.T, self.Nc, self.B, self.codes
        snr_dBs = linspace(params.snrfrom, params.to, params.len)
        sigmav2s = 1.0 / inv_dB(snr_dBs)

        amis = zeros(len(snr_dBs))
        for i in trange(len(snr_dBs)):
            sum_outer = 0.0
            for _ in range(IT):
                V = sqrt(sigmav2s[i]) * randn_c(N, T)
                # V = sqrt(sigmav2) * seedv.reshape(M, 1) # for debug
                self.channel.randomize()
                H = self.channel.getChannel()  # N \times M
                for outer in range(Nc):
                    sum_inner = 0.0
                    for inner in range(Nc):
                        hxy = matmul(H, codes[outer] - codes[inner])
                        head = hxy + V
                        tail = V
                        coeff = (-power(linalg.norm(head), 2) + power(linalg.norm(tail), 2)) / sigmav2s[i]
                        sum_inner += exp(coeff)
                    sum_outer += log2(sum_inner)
            # print("bminus = " + str(sum_outer / Nc / IT))
            amis[i] = (B - sum_outer / Nc / IT) / T
            if printValue:
                print("At SNR = %1.2f dB, AMI = %1.10f" % (snr_dBs[i], amis[i]))

        ret = self.dicToNumpy({"snr_dB": snr_dBs, "ami": amis})
        if outputFile:
            print(ret)
            self.saveCSV(params.arg, ret)
        return ret

    def simulateAMIParallel(self, params, outputFile=True, printValue=True):
        """Simulates AMI values at multiple SNRs, where the massively parallel algorithm is used. This implementation is especially designed for cupy.

        Args:
            params (imtoolkit.Parameter): simulation parameters.
            outputFile (bool): a flag that determines whether to output the obtained results to the results/ directory.
            printValue (bool): a flag that determines whether to print the simulated values.

        Returns:
            dict: a dict that has two keys: snr_dB and ami, and contains the corresponding results. All the results are transferred into the CPU memory.
        """

        M, N, T, ITo, ITi, Nc, B, codes = params.M, params.N, params.T, params.ITo, params.ITi, self.Nc, self.B, self.codes
        snr_dBs = linspace(params.snrfrom, params.to, params.len)
        lsnr = len(snr_dBs)
        sigmav2s = 1.0 / inv_dB(snr_dBs)
        sigmav2stensor = repeat(sigmav2s, ITi * Nc * Nc).reshape(lsnr, ITi, Nc, Nc)

        # The following three variables are the same as those used in simulateBERParallel
        x = hstack(tile(codes, Nc))  # M \times T * Nc^2
        y = tile(hstack(codes), Nc)  # M \times T * Nc^2
        diffxy = x - y  # M \times T * Nc^2

        amis = zeros(len(snr_dBs))
        for ito in trange(ITo):
            self.channel.randomize()
            Ho = self.channel.getChannel().reshape(ITi, N, M)  # ITi \times N \times M
            Vo = tile(randn_c(ITi, N, T), Nc ** 2)  # ITi \times N \times T * Nc**2
            bigh = zeros((lsnr, ITi, N, M), dtype=complex)  # lsnr \times ITi \times N \times M
            bigv = zeros((lsnr, ITi, N, T * Nc ** 2), dtype=complex)  # lsnr \times ITi \times N \times T * Nc**2
            for i in range(lsnr):
                bigh[i] = Ho
                bigv[i] = sqrt(sigmav2s[i]) * Vo

            bigvfro = power(abs(bigv), 2).reshape(lsnr, ITi, N, Nc ** 2, T)  # lsnr \times ITi \times N \times Nc**2 \times T
            frov = sum(bigvfro, axis=(2, 4)).reshape(lsnr, ITi, Nc, Nc)  # lsnr \times ITi \times Nc \times Nc
            hsplusv = matmul(bigh, diffxy) + bigv  # lsnr \times ITi \times N \times T * Nc^2
            hsvfro = power(abs(hsplusv), 2).reshape(lsnr, ITi, N, Nc * Nc, T)  # lsnr \times ITi \times N \times Nc**2 \times T
            froy = sum(hsvfro, axis=(2, 4))  # lsnr \times ITi \times Nc^2
            reds = froy.reshape(lsnr, ITi, Nc, Nc)  # lsnr \times ITi \times Nc \times Nc
            ecoffs = (-reds + frov) / sigmav2stensor  # diagonal elements must be zero
            bminus = mean(log2(sum(exp(ecoffs), axis=3)), axis=(1, 2))
            amis += (B - bminus) / T
            if printValue:
                for i in range(len(snr_dBs)):
                    print("At SNR = %1.2f dB, AMI = %1.10f" % (snr_dBs[i], amis[i] / (ito + 1)))

        #
        amis /= ITo
        ret = self.dicToNumpy({"snr_dB": snr_dBs, "ami": amis})
        if outputFile:
            print(ret)
            self.saveCSV(params.arg, ret)

        return ret

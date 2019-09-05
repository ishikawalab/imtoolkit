# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import os
import pandas as pd

if os.getenv("USECUPY") == "1":
    import cupy as xp
else:
    import numpy as xp


class Simulator(object):
    """A basis class for an arbitrary simulator, which has some useful functions for output simulation results.

    The input codes are stored in the host memory (numpy), while all the calculations are conducted in the device memory (cupy), if possible.
    """

    def __init__(self, codes, channel):
        """
        Args:
            codes (numpy.ndarray): the input codebook, which is an (Nc,M,T)-sized tensor.
            channel (imtoolkit.Channel): the channel class used for simulations.
        """
        self.codes = self.toXpArray(codes)  # Copy codes to the GPU memory
        self.Nc = len(codes)  # The number of codewords
        self.B = xp.log2(self.Nc)  # The bitwidth per codeword
        self.channel = channel  # The specified channel generator

    def toXpArray(self, arr):
        return xp.asarray(arr)

    @classmethod
    def dicToNumpy(self, dic):
        for key in dic.keys():
            if 'cupy' in str(type(dic[key])):
                dic[key] = xp.asnumpy(dic[key])
        return dic

    @classmethod
    def dicToDF(self, dic):
        for key in dic.keys():
            if 'cupy' in str(type(dic[key])):
                dic[key] = xp.asnumpy(dic[key])
        return pd.DataFrame(dic)

    @classmethod
    def saveCSV(self, arg, df):
        if not os.path.exists("results/"):
            os.mkdir("results/")
        fname = "results/" + arg + ".csv"
        if 'dic' in str(type(df)):
            df = pd.DataFrame(df)
        df.to_csv(fname, index=False, float_format="%.20e")
        # np.savetxt(fname, np.c_[x, y], delimiter = ",", header = xlabel + "," + ylabel)
        print("The above results were saved to " + fname)

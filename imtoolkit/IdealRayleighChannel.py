# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

from numba import jitclass, int64, complex128
from .Channel import Channel
from .Util import randn_c

@jitclass([('IT', int64), ('M', int64), ('N', int64), ('channelMatrix', complex128[:,:])])
class IdealRayleighChannel(Channel):
    """
    A `Channel` class that generates the ideal Rayleigh fading channel coefficients.
    """
    def __init__(self, IT, M, N):
        """
        Args:
            IT (int): the number of parallel channel matrices.
            M (int): the number of transmit antennas.
            N (int):the number of receive antennas.
        """
        self.IT = IT
        self.M = M
        self.N = N
    
    def randomize(self):
        self.channelMatrix = randn_c(self.IT * self.N, self.M)
    
    def getChannel(self):
        return self.channelMatrix

    def getEstimate(self):
        # Perfect channel state informaiton at the receiver
        return self.channelMatrix



# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

from numba import jitclass, int64, complex128
from .Channel import Channel
from .Util import xp, randn_c


@jitclass([('IT', int64), ('M', int64), ('N', int64), ('channelMatrix', complex128[:,:])])
class AWGNChannel(Channel):
    """
    A `Channel` class that generates the additive white Gaussian noise (AWGN). All the channel matrix is set to an identity matrix.
    """

    def __init__(self, IT, M):
        """
        Args:
            IT (int): the number of parallel channel matrices.
            M (int): the number of transmit antennas or subcarriers.
        """
        self.IT = IT
        self.M = M
        self.N = M
    
    def randomize(self):
        self.channelMatrix = xp.tile(xp.eye(self.M), self.IT).T
    
    def getChannel(self):
        return self.channelMatrix

    def getEstimate(self):
        return self.channelMatrix

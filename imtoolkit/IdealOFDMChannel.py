# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

from numba import jitclass, int64, complex128
from .Channel import Channel
from .Util import xp, randn_c


@jitclass([('IT', int64), ('M', int64), ('channelMatrix', complex128[:,:])])
class IdealOFDMChannel(Channel):
    """
        A `Channel` class that generates the ideal OFDM channel coefficients. All the channel matrix is set to a diagonal matrix of `M` Rayleigh coefficients.
    """

    def __init__(self, IT, M):
        """
        Args:
            IT (int): the number of parallel channel matrices.
            M (int): the number of subcarriers.
        """
        self.IT = IT
        self.M = M
    
    def randomize(self):
        self.channelMatrix = (xp.tile(xp.eye(self.M), self.IT) * randn_c(self.IT * self.M)).T
    
    def getChannel(self):
        return self.channelMatrix

    def getEstimate(self):
        # Perfect channel state informaiton at the receiver
        return self.channelMatrix

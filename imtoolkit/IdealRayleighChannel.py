# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

from .Channel import *
from .Util import *

class IdealRayleighChannel(Channel):

    def __init__(self, IT, M, N):
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



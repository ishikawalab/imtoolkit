# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

from .Channel import *
from .Util import *

class IdealOFDMChannel(Channel):

    def __init__(self, IT, M):
        self.IT = IT
        self.M = M
    
    def randomize(self):
        self.channelMatrix = (tile(eye(self.M), self.IT) * randn_c(self.IT * self.M)).T
    
    def getChannel(self):
        return self.channelMatrix

    def getEstimate(self):
        # Perfect channel state informaiton at the receiver
        return self.channelMatrix

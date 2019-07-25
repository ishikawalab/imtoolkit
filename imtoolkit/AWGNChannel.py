# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

from .Channel import Channel
from .Util import xp, randn_c

class AWGNChannel(Channel):

    def __init__(self, IT, M):
        self.IT = IT
        self.M = M
    
    def randomize(self):
        self.channelMatrix = xp.tile(xp.eye(self.M), self.IT).T
    
    def getChannel(self):
        return self.channelMatrix

    def getEstimate(self):
        return self.channelMatrix

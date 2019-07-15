# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
import numpy as np
from imtoolkit.Parameters import *
from imtoolkit.OSTBCode import *
from imtoolkit.Modulator import *
from imtoolkit.IdealRayleighChannel import *
from imtoolkit.SemiUnitaryDifferentialMLDSimulator import *

class SemiUnitaryDifferentialMLDSimulatorTest(unittest.TestCase):

    def test_BERReference_SQAM(self):
        truth = np.log10(np.array([3.94573999999999980304e-01,3.05669000000000024020e-01,2.02045000000000002371e-01,1.10306000000000001271e-01,4.76810000000000011600e-02,1.77129999999999995786e-02,6.14199999999999989020e-03]))
        params = Parameters("BER_sim=sudiff_channel=rayleigh_M=1_N=1_L=16_mod=SQAM_IT=1e5_snrfrom=0.00_to=30.00_len=7")
        codes = Modulator(params.mod, params.L).symbols.reshape(params.L, 1, 1)
        channel = IdealRayleighChannel(1, params.M, params.N)
        sim = SemiUnitaryDifferentialMLDSimulator(codes, channel)
        ret = sim.simulateBERReference(params, output = False)
        retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
        self.assertLessEqual(retnorm, 1e-2)

    def test_BERParallel_SQAM(self):
        truth = np.log10(np.array([3.94573999999999980304e-01,3.05669000000000024020e-01,2.02045000000000002371e-01,1.10306000000000001271e-01,4.76810000000000011600e-02,1.77129999999999995786e-02,6.14199999999999989020e-03]))
        params = Parameters("BER_sim=sudiff_channel=rayleigh_M=1_N=1_L=16_mod=SQAM_ITo=1e1_ITi=1e4_snrfrom=0.00_to=30.00_len=7")
        codes = Modulator(params.mod, params.L).symbols.reshape(params.L, 1, 1)
        channel = IdealRayleighChannel(params.ITi, params.M, params.N)
        sim = SemiUnitaryDifferentialMLDSimulator(codes, channel)
        ret = sim.simulateBERParallel(params, output = False)
        retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
        self.assertLessEqual(retnorm, 1e-2)

if __name__ == '__main__':
    unittest.main()

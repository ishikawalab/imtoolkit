# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
import numpy as np
from imtoolkit.Parameters import *
from imtoolkit.OSTBCode import *
from imtoolkit.IdealRayleighChannel import *
from imtoolkit.DifferentialMLDSimulator import *

class DifferentialMLDSimulatorTest(unittest.TestCase):

    def test_BERReference_OSTBC(self):
        truth = np.log10(np.array([4.30007799999999995588e-01,3.16763799999999984269e-01,1.40630900000000003125e-01,2.39459999999999985365e-02,1.21079999999999994055e-03]))
        #params = Parameters("BER_sim=diff_channel=rayleigh_code=OSTBC_M=2_N=2_T=2_L=2_mod=PSK_IT=1e4_snrfrom=-10.00_to=10.00_len=5")
        params = Parameters("BER_sim=diff_channel=rayleigh_code=OSTBC_M=2_N=2_T=2_L=2_mod=PSK_IT=1e6_snrfrom=-10.00_to=10.00_len=5")
        code = OSTBCode(params.M, "PSK", params.L)
        channel = IdealRayleighChannel(1, params.M, params.N)
        sim = DifferentialMLDSimulator(code.codes, channel)
        ret = sim.simulateBERReference(params, output = False)
        retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
        self.assertLessEqual(retnorm, 1e-2)
    
    def test_BERParallel_OSTBC(self):
        np.set_printoptions(linewidth=np.inf)
        truth = np.log10(np.array([4.30007799999999995588e-01,3.16763799999999984269e-01,1.40630900000000003125e-01,2.39459999999999985365e-02,1.21079999999999994055e-03]))
        params = Parameters("BERP_sim=diff_channel=rayleigh_code=OSTBC_M=2_N=2_T=2_L=2_mod=PSK_ITo=1e1_ITi=1e6_snrfrom=-10.00_to=10.00_len=5")
        #params = Parameters("BERP_sim=diff_channel=rayleigh_code=OSTBC_M=2_N=2_T=2_L=2_mod=PSK_ITo=1_ITi=9_snrfrom=-10.00_to=10.00_len=5")
        #params = Parameters("BERP_sim=diff_channel=rayleigh_code=OSTBC_M=2_N=2_T=2_L=2_mod=PSK_ITo=1_ITi=9_snrfrom=50.00_to=50.00_len=1")
        code = OSTBCode(params.M, "PSK", params.L)
        channel = IdealRayleighChannel(params.ITi, params.M, params.N)
        sim = DifferentialMLDSimulator(code.codes, channel)
        ret = sim.simulateBERParallel(params, output = False)
        retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
        self.assertLessEqual(retnorm, 1e-2)
        
if __name__ == '__main__':
    unittest.main()

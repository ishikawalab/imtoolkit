# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
import numpy as np
from imtoolkit.Parameters import *
from imtoolkit.OSTBCode import *
from imtoolkit.DiagonalUnitaryCode import *
from imtoolkit.ADSMCode import *
from imtoolkit.IdealRayleighChannel import *
from imtoolkit.DifferentialMLDSimulator import *

class DifferentialMLDSimulatorTest(unittest.TestCase):

    def test_BERReference_OSTBC(self):
        truth = np.log10(np.array([4.30007799999999995588e-01,3.16763799999999984269e-01,1.40630900000000003125e-01,2.39459999999999985365e-02,1.21079999999999994055e-03]))
        params = Parameters("BER_sim=diff_channel=rayleigh_code=OSTBC_M=2_N=2_T=2_L=2_mod=PSK_IT=1e4_snrfrom=-10.00_to=10.00_len=5")
        #params = Parameters("BER_sim=diff_channel=rayleigh_code=OSTBC_M=2_N=2_T=2_L=2_mod=PSK_IT=1e6_snrfrom=-10.00_to=10.00_len=5")
        code = OSTBCode(params.M, "PSK", params.L)
        channel = IdealRayleighChannel(1, params.M, params.N)
        sim = DifferentialMLDSimulator(code.codes, channel)
        ret = sim.simulateBERReference(params, output = False)
        retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
        self.assertLessEqual(retnorm, 1e-2)
    
    def test_BERParallel_OSTBC(self):
        np.set_printoptions(linewidth=np.inf)
        truth = np.log10(np.array([4.30007799999999995588e-01,3.16763799999999984269e-01,1.40630900000000003125e-01,2.39459999999999985365e-02,1.21079999999999994055e-03]))
        params = Parameters("BERP_sim=diff_channel=rayleigh_code=OSTBC_M=2_N=2_T=2_L=2_mod=PSK_ITo=1e1_ITi=1e3_snrfrom=-10.00_to=10.00_len=5")
        #params = Parameters("BERP_sim=diff_channel=rayleigh_code=OSTBC_M=2_N=2_T=2_L=2_mod=PSK_ITo=1e1_ITi=1e6_snrfrom=-10.00_to=10.00_len=5")
        code = OSTBCode(params.M, "PSK", params.L)
        channel = IdealRayleighChannel(params.ITi, params.M, params.N)
        sim = DifferentialMLDSimulator(code.codes, channel)
        ret = sim.simulateBERParallel(params, output = False)
        retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
        self.assertLessEqual(retnorm, 1e-2)
    
    def test_BERReference_DUC(self):
        truth = np.log10(np.array([4.86660099999999984366e-01,4.48927299999999973590e-01,3.32694099999999992612e-01,1.44086500000000006239e-01,2.63749999999999991396e-02]))
        params = Parameters("BER_sim=diff_channel=rayleigh_code=DUC_M=2_L=16_N=2_T=2_IT=1e5_snrfrom=-10.00_to=10.00_len=5")
        code = DiagonalUnitaryCode(params.M, params.L)
        channel = IdealRayleighChannel(1, params.M, params.N)
        sim = DifferentialMLDSimulator(code.codes, channel)
        ret = sim.simulateBERReference(params, output = False)
        retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
        self.assertLessEqual(retnorm, 1e-2)

    def test_BERParallel_DUC(self):
        truth = np.log10(np.array([4.86660099999999984366e-01,4.48927299999999973590e-01,3.32694099999999992612e-01,1.44086500000000006239e-01,2.63749999999999991396e-02]))
        params = Parameters("BERP_sim=diff_channel=rayleigh_code=DUC_M=2_L=16_N=2_T=2_ITo=1e1_ITi=1e4_snrfrom=-10.00_to=10.00_len=5")
        code = DiagonalUnitaryCode(params.M, params.L)
        channel = IdealRayleighChannel(params.ITi, params.M, params.N)
        sim = DifferentialMLDSimulator(code.codes, channel)
        ret = sim.simulateBERParallel(params, output = False)
        retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
        self.assertLessEqual(retnorm, 1e-2)

    def test_BERReference_ADSM(self):
        truth = np.log10(np.array([3.23886999999999980471e-01,1.08588000000000003964e-01,1.21379999999999994842e-02,5.29999999999999980675e-04]))
        params = Parameters("BER_sim=diff_channel=rayleigh_code=ADSM_M=4_L=4_mod=PSK_T=4_N=1_IT=1e5_snrfrom=0.00_to=15.00_len=4")
        code = ADSMCode(params.M, "PSK", params.L)
        channel = IdealRayleighChannel(1, params.M, params.N)
        sim = DifferentialMLDSimulator(code.codes, channel)
        ret = sim.simulateBERReference(params, output = False)
        retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
        self.assertLessEqual(retnorm, 1e-2)
    
    def test_BERParallel_ADSM(self):
        truth = np.log10(np.array([3.23886999999999980471e-01,1.08588000000000003964e-01,1.21379999999999994842e-02,5.29999999999999980675e-04]))
        params = Parameters("BERP_sim=diff_channel=rayleigh_code=ADSM_M=4_L=4_mod=PSK_T=4_N=1_ITo=1e1_ITi=1e4_snrfrom=0.00_to=15.00_len=4")
        code = ADSMCode(params.M, "PSK", params.L)
        channel = IdealRayleighChannel(params.ITi, params.M, params.N)
        sim = DifferentialMLDSimulator(code.codes, channel)
        ret = sim.simulateBERParallel(params, output = False)
        retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
        self.assertLessEqual(retnorm, 1e-2)

if __name__ == '__main__':
    unittest.main()

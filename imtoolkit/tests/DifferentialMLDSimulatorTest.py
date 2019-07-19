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
        ret = sim.simulateBERReference(params, outputFile = False)
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
        ret = sim.simulateBERParallel(params, outputFile = False)
        retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
        self.assertLessEqual(retnorm, 1e-2)
    
    def test_BERReference_DUC(self):
        truth = np.log10(np.array([4.86660099999999984366e-01,4.48927299999999973590e-01,3.32694099999999992612e-01,1.44086500000000006239e-01,2.63749999999999991396e-02]))
        params = Parameters("BER_sim=diff_channel=rayleigh_code=DUC_M=2_L=16_N=2_T=2_IT=1e5_snrfrom=-10.00_to=10.00_len=5")
        code = DiagonalUnitaryCode(params.M, params.L)
        channel = IdealRayleighChannel(1, params.M, params.N)
        sim = DifferentialMLDSimulator(code.codes, channel)
        ret = sim.simulateBERReference(params, outputFile = False)
        retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
        self.assertLessEqual(retnorm, 1e-2)

    # Heavy test, somehow failed
    # def test_BERReference_DUC_largeL(self):
    #     truth = np.log10(np.array([3.67063492063492036177e-01,2.95634920634920639326e-01,2.29166666666666657415e-01,1.79563492063492063933e-01,1.36904761904761917979e-01,7.53968253968253926400e-02,4.06746031746031758147e-02,8.92857142857142807579e-03,9.92063492063492008421e-04]))
    #     params = Parameters("BER_sim=diff_channel=rayleigh_code=DUC_M=4_L=65536_N=4_T=4_IT=1e3_snrfrom=00.00_to=40.00_len=9")
    #     code = DiagonalUnitaryCode(params.M, params.L)
    #     channel = IdealRayleighChannel(1, params.M, params.N)
    #     sim = DifferentialMLDSimulator(code.codes, channel)
    #     ret = sim.simulateBERReference(params, outputFile = False, printValue = True)
    #     print(ret)
    #     retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
    #     self.assertLessEqual(retnorm, 1e-2)

    def test_BERParallel_DUC(self):
        truth = np.log10(np.array([4.86660099999999984366e-01,4.48927299999999973590e-01,3.32694099999999992612e-01,1.44086500000000006239e-01,2.63749999999999991396e-02]))
        params = Parameters("BERP_sim=diff_channel=rayleigh_code=DUC_M=2_L=16_N=2_T=2_ITo=1e1_ITi=1e4_snrfrom=-10.00_to=10.00_len=5")
        code = DiagonalUnitaryCode(params.M, params.L)
        channel = IdealRayleighChannel(params.ITi, params.M, params.N)
        sim = DifferentialMLDSimulator(code.codes, channel)
        ret = sim.simulateBERParallel(params, outputFile = False)
        retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
        self.assertLessEqual(retnorm, 1e-2)

    def test_BERReference_ADSM(self):
        truth = np.log10(np.array([3.23886999999999980471e-01,1.08588000000000003964e-01,1.21379999999999994842e-02,5.29999999999999980675e-04]))
        params = Parameters("BER_sim=diff_channel=rayleigh_code=ADSM_M=4_L=4_mod=PSK_T=4_N=1_IT=1e5_snrfrom=0.00_to=15.00_len=4")
        code = ADSMCode(params.M, "PSK", params.L)
        channel = IdealRayleighChannel(1, params.M, params.N)
        sim = DifferentialMLDSimulator(code.codes, channel)
        ret = sim.simulateBERReference(params, outputFile = False)
        retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
        self.assertLessEqual(retnorm, 1e-2)

    # Heavy test
    # def test_BERReference_ADSM_largeL(self):
    #     truth = np.log10(np.array([4.16666666666666685170e-01,3.43253968253968255731e-01,3.34325396825396803369e-01,2.76785714285714301575e-01,2.75793650793650813036e-01,2.60912698412698429440e-01,2.31150793650793662248e-01,2.07341269841269854046e-01,1.60714285714285726181e-01,1.34920634920634913145e-01,1.19047619047619041011e-01]))
    #     params = Parameters("BER_sim=diff_channel=rayleigh_code=ADSM_M=4_L=16384_mod=PSK_N=4_T=4_IT=1e2_snrfrom=00.00_to=50.00_len=11")
    #     code = ADSMCode(params.M, params.mod, params.L)
    #     channel = IdealRayleighChannel(1, params.M, params.N)
    #     sim = DifferentialMLDSimulator(code.codes, channel)
    #     ret = sim.simulateBERReference(params, outputFile = False, printValue = True)
    #     print(ret)
    #     retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
    #     self.assertLessEqual(retnorm, 1e-2)    

    def test_BERParallel_ADSM(self):
        truth = np.log10(np.array([3.23886999999999980471e-01,1.08588000000000003964e-01,1.21379999999999994842e-02,5.29999999999999980675e-04]))
        params = Parameters("BERP_sim=diff_channel=rayleigh_code=ADSM_M=4_L=4_mod=PSK_T=4_N=1_ITo=1e1_ITi=1e4_snrfrom=0.00_to=15.00_len=4")
        code = ADSMCode(params.M, "PSK", params.L)
        channel = IdealRayleighChannel(params.ITi, params.M, params.N)
        sim = DifferentialMLDSimulator(code.codes, channel)
        ret = sim.simulateBERParallel(params, outputFile = False)
        retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
        self.assertLessEqual(retnorm, 1e-2)

if __name__ == '__main__':
    unittest.main()

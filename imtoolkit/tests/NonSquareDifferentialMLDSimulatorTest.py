# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
import numpy as np
from imtoolkit import Parameters, OSTBCode, AWGNChannel, IdealRayleighChannel, Basis, NonSquareDifferentialMLDSimulator

class NonSquareDifferentialMLDSimulatorTest(unittest.TestCase):

    def test_BERReference_NDOSTC_AWGN(self):
       truth = np.log10(np.array([4.90489052631578936747e-01,4.68008763157894747131e-01,3.89989789473684234089e-01,1.77222684210526310045e-01,8.28273684210526286997e-03]))
       params = Parameters("BER_sim=nsdiff_channel=AWGN_code=OSTBC_basis=i_M=2_N=2_T=1_L=2_W=40_IT=1e4_snrfrom=-10.00_to=10.00_len=5")
       codes = OSTBCode(params.M, params.mod, params.L).codes
       channel = AWGNChannel(1, params.M)
       bases = Basis(params.basis, params.M, params.T).bases
       sim = NonSquareDifferentialMLDSimulator(codes, channel, bases)
       ret = sim.simulateBERReference(params, outputFile = False)
       retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
       self.assertLessEqual(retnorm, 1e-2)

    def test_BERReference_NDOSTC_Rayleigh(self):
       truth = np.log10(np.array([4.80833947368421055213e-01,4.41299473684210519231e-01,3.40417894736842086001e-01,1.59756578947368416133e-01,3.54696052631578925829e-02,4.77671052631578954561e-03]))
       params = Parameters("BER_sim=nsdiff_channel=rayleigh_code=OSTBC_basis=i_M=2_N=2_T=1_L=2_W=40_IT=1e4_snrfrom=-10.00_to=15.00_len=6")
       codes = OSTBCode(params.M, params.mod, params.L).codes
       channel = IdealRayleighChannel(1, params.M, params.N)
       bases = Basis(params.basis, params.M, params.T).bases
       sim = NonSquareDifferentialMLDSimulator(codes, channel, bases)
       ret = sim.simulateBERReference(params, outputFile = False)
       retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
       self.assertLessEqual(retnorm, 1e-2)

    def test_BERParallel_NDOSTC_AWGN(self):
        truth = np.log10(np.array([4.90489052631578936747e-01,4.68008763157894747131e-01,3.89989789473684234089e-01,1.77222684210526310045e-01,8.28273684210526286997e-03]))
        params = Parameters("BER_sim=nsdiff_channel=AWGN_code=OSTBC_basis=i_M=2_N=2_T=1_L=2_W=40_ITo=1e1_ITi=1e3_snrfrom=-10.00_to=10.00_len=5")
        #params = Parameters("BER_sim=nsdiff_channel=AWGN_code=OSTBC_basis=i_M=2_N=2_T=1_L=2_W=40_ITo=1e1_ITi=1e2_snrfrom=100.00_to=100.00_len=1")
        codes = OSTBCode(params.M, params.mod, params.L).codes
        channel = AWGNChannel(params.ITi, params.M)
        bases = Basis(params.basis, params.M, params.T).bases
        sim = NonSquareDifferentialMLDSimulator(codes, channel, bases)
        ret = sim.simulateBERParallel(params, outputFile = False, printValue = False)
        retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
        self.assertLessEqual(retnorm, 1e-2)

    def test_BERParallel_NDOSTC(self):
        truth = np.log10(np.array([4.80833947368421055213e-01,4.41299473684210519231e-01,3.40417894736842086001e-01,1.59756578947368416133e-01,3.54696052631578925829e-02,4.77671052631578954561e-03]))
        params = Parameters("BER_sim=nsdiff_channel=rayleigh_code=OSTBC_basis=i_M=2_N=2_T=1_L=2_W=40_ITo=1_ITi=1e5_snrfrom=-10.00_to=15.00_len=6")
        codes = OSTBCode(params.M, params.mod, params.L).codes
        channel = IdealRayleighChannel(params.ITi, params.M, params.N)
        bases = Basis(params.basis, params.M, params.T).bases
        sim = NonSquareDifferentialMLDSimulator(codes, channel, bases)
        ret = sim.simulateBERParallel(params, outputFile = False, printValue = False)
        retnorm = np.mean(np.power(np.abs(np.log10(ret["ber"]) - truth), 2))
        self.assertLessEqual(retnorm, 1e-2)

if __name__ == '__main__':
    unittest.main()

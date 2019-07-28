# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
import numpy as np
from imtoolkit import Parameters, Modulator, OSTBCode, TASTCode, IdealRayleighChannel, SemiUnitaryDifferentialMLDSimulator

class SemiUnitaryDifferentialMLDSimulatorTest(unittest.TestCase):

    def test_BERReference_SQAM(self):
        truth = np.log10(np.array([3.94573999999999980304e-01,3.05669000000000024020e-01,2.02045000000000002371e-01,1.10306000000000001271e-01,4.76810000000000011600e-02,1.77129999999999995786e-02,6.14199999999999989020e-03]))
        params = Parameters("BER_sim=sudiff_channel=rayleigh_M=1_N=1_L=16_mod=SQAM_IT=1e5_snrfrom=0.00_to=30.00_len=7")
        codes = Modulator(params.mod, params.L).symbols.reshape(params.L, 1, 1)
        channel = IdealRayleighChannel(1, params.M, params.N)
        sim = SemiUnitaryDifferentialMLDSimulator(codes, channel)
        ret = sim.simulateBERReference(params, outputFile = False)
        np.testing.assert_almost_equal(np.log10(ret["ber"]), truth, 1)

    def test_BERParallel_SQAM(self):
        truth = np.log10(np.array([3.94573999999999980304e-01,3.05669000000000024020e-01,2.02045000000000002371e-01,1.10306000000000001271e-01,4.76810000000000011600e-02,1.77129999999999995786e-02,6.14199999999999989020e-03]))
        params = Parameters("BER_sim=sudiff_channel=rayleigh_M=1_N=1_L=16_mod=SQAM_ITo=1e1_ITi=1e4_snrfrom=0.00_to=30.00_len=7")
        codes = Modulator(params.mod, params.L).symbols.reshape(params.L, 1, 1)
        channel = IdealRayleighChannel(params.ITi, params.M, params.N)
        sim = SemiUnitaryDifferentialMLDSimulator(codes, channel)
        ret = sim.simulateBERParallel(params, outputFile = False)
        np.testing.assert_almost_equal(np.log10(ret["ber"]), truth, 1)

    def test_BERReference_TAST(self):
        truth = np.log10(np.array([4.42719114561770876737e-01,3.35158329683340638905e-01,1.74362651274697438852e-01,4.47959104081791861796e-02,4.18899162201675622635e-03]))
        params = Parameters("BER_sim=sudiff_channel=rayleigh_code=TAST_M=2_T=2_Q=2_L=16_mod=SQAM_N=2_IT=1e5_snrfrom=0.00_to=20.00_len=5")
        codes = TASTCode(params.M, params.Q, params.L).codes
        channel = IdealRayleighChannel(1, params.M, params.N)
        sim = SemiUnitaryDifferentialMLDSimulator(codes, channel)
        ret = sim.simulateBERReference(params, outputFile = False)
        np.testing.assert_almost_equal(np.log10(ret["ber"]), truth, 1)

    def test_BERParallel_TAST(self):
        truth = np.log10(np.array([4.42719114561770876737e-01,3.35158329683340638905e-01,1.74362651274697438852e-01,4.47959104081791861796e-02,4.18899162201675622635e-03]))
        params = Parameters("BERP_sim=sudiff_channel=rayleigh_code=TAST_M=2_T=2_Q=2_L=16_mod=SQAM_N=2_ITo=1e1_ITi=1e4_snrfrom=0.00_to=20.00_len=5")
        codes = TASTCode(params.M, params.Q, params.L).codes
        channel = IdealRayleighChannel(params.ITi, params.M, params.N)
        sim = SemiUnitaryDifferentialMLDSimulator(codes, channel)
        ret = sim.simulateBERParallel(params, outputFile = False)
        np.testing.assert_almost_equal(np.log10(ret["ber"]), truth, 1)

if __name__ == '__main__':
    unittest.main()

# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
import numpy as np
from imtoolkit import Parameters, IMCode, OSTBCode, IdealRayleighChannel, CoherentMLDSimulator, Basis

class CoherentMLDSimulatorTest(unittest.TestCase):

    def test_BERReference_SM(self):
        truth = np.log10(np.array([3.39290432141913567143e-01,2.28799154240169139163e-01,1.16562376687524657526e-01,4.63410907317818518414e-02,1.58151968369606328590e-02,5.27619894476021120827e-03,1.64459967108006571007e-03]))
        params = Parameters("BER_sim=coh_code=index_dm=dic_M=2_K=1_Q=2_L=4_mod=PSK_N=1_IT=1e5_snrfrom=0.00_to=30.00_len=7")
        code = IMCode(params.dm, params.M, params.K, params.Q, params.mod, params.L, meanPower = 1)
        channel = IdealRayleighChannel(1, params.M, params.N)
        sim = CoherentMLDSimulator(code.codes, channel)
        ret = sim.simulateBERReference(params, outputFile = False, printValue = False)
        np.testing.assert_almost_equal(np.log10(ret["ber"]), truth, 1)
    
    def test_BERParallel_SM(self):
        truth = np.log10(np.array([3.39290432141913567143e-01,2.28799154240169139163e-01,1.16562376687524657526e-01,4.63410907317818518414e-02,1.58151968369606328590e-02,5.27619894476021120827e-03,1.64459967108006571007e-03]))
        params = Parameters("BERP_sim=coh_code=index_dm=dic_M=2_K=1_Q=2_L=4_mod=PSK_N=1_ITo=1e1_ITi=1e4_snrfrom=0.00_to=30.00_len=7")
        #params = Parameters("BERP_sim=coh_code=index_dm=dic_M=2_K=1_Q=2_L=1_mod=PSK_N=1_ITo=1_ITi=55_snrfrom=0.00_to=30.00_len=7")
        code = IMCode(params.dm, params.M, params.K, params.Q, params.mod, params.L, meanPower = 1)
        channel = IdealRayleighChannel(params.ITi, params.M, params.N)
        sim = CoherentMLDSimulator(code.codes, channel)
        ret = sim.simulateBERParallel(params, outputFile = False, printValue = False)
        np.testing.assert_almost_equal(np.log10(ret["ber"]), truth, 1)

    # Heavy test
    # def test_BERParallel_SM_M4(self):
    #     truth = np.log10(np.array([1.50814659999999989282e-01,2.28938300000000004297e-02,8.41559999999999986016e-04,1.20200000000000001125e-05,1.40000000000000009547e-07]))
    #     params = Parameters("BERP_sim=coh_channel=rayleigh_code=index_dm=opt_M=4_N=4_T=1_Q=4_L=4_ITo=1e4_ITi=1e4_snrfrom=0.00_to=20.00_len=5")
    #     code = IMCode(params.dm, params.M, params.K, params.Q, params.mod, params.L, meanPower = 1)
    #     channel = IdealRayleighChannel(params.ITi, params.M, params.N)
    #     sim = CoherentMLDSimulator(code.codes, channel)
    #     ret = sim.simulateBERParallel(params, outputFile = False, printValue = False)
    #     np.testing.assert_almost_equal(np.log10(ret["ber"]), truth, 1)

    def test_AMIReference_SM(self):
        truth = np.array([1.42818014515766478212e-02,4.46896133972787268362e-02,1.35020118355007934241e-01,3.74152908820060137174e-01,8.88430916560169148255e-01,1.63202684937455133607e+00,2.32075268455922545385e+00,2.73556303528255551072e+00,2.90887984047466385817e+00])
        params = Parameters("AMI_sim=coh_code=index_dm=dic_M=2_K=1_Q=2_L=4_mod=PSK_N=1_IT=1e3_snrfrom=-20.00_to=20.00_len=9")
        code = IMCode(params.dm, params.M, params.K, params.Q, params.mod, params.L, meanPower = 1)
        channel = IdealRayleighChannel(1, params.M, params.N)
        sim = CoherentMLDSimulator(code.codes, channel)
        ret = sim.simulateAMIReference(params, outputFile = False, printValue = False)
        np.testing.assert_almost_equal(ret["ami"], truth, 1)

    def test_AMIParallel_SM(self):
        truth = np.array([1.42818014515766478212e-02,4.46896133972787268362e-02,1.35020118355007934241e-01,3.74152908820060137174e-01,8.88430916560169148255e-01,1.63202684937455133607e+00,2.32075268455922545385e+00,2.73556303528255551072e+00,2.90887984047466385817e+00])
        params = Parameters("AMIP_sim=coh_code=index_dm=dic_M=2_K=1_Q=2_L=4_mod=PSK_N=1_ITo=1e1_ITi=1e4_snrfrom=-20.00_to=20.00_len=9")
        code = IMCode(params.dm, params.M, params.K, params.Q, params.mod, params.L, meanPower = 1)
        channel = IdealRayleighChannel(params.ITi, params.M, params.N)
        sim = CoherentMLDSimulator(code.codes, channel)
        ret = sim.simulateAMIParallel(params, outputFile = False, printValue = False)
        np.testing.assert_almost_equal(ret["ami"], truth, 1)

    def test_BERReference_OSTBC(self):
        truth = np.log10(np.array([2.72212300000000018141e-01,1.46606500000000000705e-01,4.03784000000000017905e-02,3.73150000000000000785e-03]))
        params = Parameters("BER_sim=coh_channel=rayleigh_code=OSTBC_M=2_N=2_T=2_L=2_mod=PSK_IT=1e5_snrfrom=-10.00_to=5.00_len=4")
        code = OSTBCode(params.M, "PSK", params.L)
        channel = IdealRayleighChannel(1, params.M, params.N)
        sim = CoherentMLDSimulator(code.codes, channel)
        ret = sim.simulateBERReference(params, outputFile = False, printValue = False)
        np.testing.assert_almost_equal(np.log10(ret["ber"]), truth, 1)

    def test_BERParallel_OSTBC(self):
        truth = np.log10(np.array([2.72212300000000018141e-01,1.46606500000000000705e-01,4.03784000000000017905e-02,3.73150000000000000785e-03]))
        params = Parameters("BERP_sim=coh_channel=rayleigh_code=OSTBC_M=2_N=2_T=2_L=2_mod=PSK_ITo=1e1_ITi=1e4_snrfrom=-10.00_to=5.00_len=4")
        code = OSTBCode(params.M, "PSK", params.L)
        channel = IdealRayleighChannel(params.ITi, params.M, params.N)
        sim = CoherentMLDSimulator(code.codes, channel)
        ret = sim.simulateBERParallel(params, outputFile = False, printValue = False)
        np.testing.assert_almost_equal(np.log10(ret["ber"]), truth, 1)

    def test_BERParallel_NDOSTC(self):
       truth = np.log10(np.array([3.43530300000000010652e-01,2.47677700000000000635e-01,1.30837700000000001221e-01,4.04209000000000026609e-02,7.00869999999999965246e-03,8.46599999999999978419e-04,9.30999999999999997046e-05]))
       params = Parameters("BERP_sim=rcoh_channel=rayleigh_code=OSTBC_basis=i_M=2_N=2_T=1_L=2_ITo=1e1_ITi=1e5_snrfrom=-10.00_to=20.00_len=7")
       codes = OSTBCode(params.M, params.mod, params.L).codes
       bases = Basis(params.basis, params.M, params.T).bases
       codes = np.matmul(codes, bases[0])
       channel = IdealRayleighChannel(params.ITi, params.M, params.N)
       from imtoolkit import CoherentMLDSimulator
       sim = CoherentMLDSimulator(codes, channel)
       ret = sim.simulateBERParallel(params, outputFile = False, printValue = False)
       np.testing.assert_almost_equal(np.log10(ret["ber"]), truth, 1)

    def test_AMIReference_OSTBC(self):
        truth = np.array([2.34009305866733186008e-01,5.31335636295124702499e-01,8.56159232876912645871e-01,9.85823618846433324947e-01,9.99561665572359148157e-01,9.99989963240521695376e-01,9.99999993834903122547e-01])
        params = Parameters("AMI_sim=coh_channel=rayleigh_code=OSTBC_M=2_N=2_T=2_L=2_mod=PSK_IT=1e3_snrfrom=-10.00_to=20.00_len=7")
        code = OSTBCode(params.M, "PSK", params.L)
        channel = IdealRayleighChannel(1, params.M, params.N)
        sim = CoherentMLDSimulator(code.codes, channel)
        ret = sim.simulateAMIReference(params, outputFile = False, printValue = False)
        np.testing.assert_almost_equal(ret["ami"], truth, 1)

    def test_AMIParallel_OSTBC(self):
        truth = np.array([2.34009305866733186008e-01,5.31335636295124702499e-01,8.56159232876912645871e-01,9.85823618846433324947e-01,9.99561665572359148157e-01,9.99989963240521695376e-01,9.99999993834903122547e-01])
        params = Parameters("AMIP_sim=coh_channel=rayleigh_code=OSTBC_M=2_N=2_T=2_L=2_mod=PSK_ITo=1e1_ITi=1e2_snrfrom=-10.00_to=20.00_len=7")
        code = OSTBCode(params.M, "PSK", params.L)
        channel = IdealRayleighChannel(params.ITi, params.M, params.N)
        sim = CoherentMLDSimulator(code.codes, channel)
        ret = sim.simulateAMIParallel(params, outputFile = False, printValue = False)
        np.testing.assert_almost_equal(ret["ami"], truth, 1)

if __name__ == '__main__':
    unittest.main()


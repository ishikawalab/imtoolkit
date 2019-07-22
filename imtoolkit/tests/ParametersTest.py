# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import unittest
from imtoolkit import Parameters

class ParametersTest(unittest.TestCase):
    def test_Parameters(self):
        arg = "BER_sim=coh_channel=rayleigh_M=1_N=1_L=2_mod=PSK_IT=1e7_snrfrom=00.00_to=50.00_len=11"
        params = Parameters(arg)
        
        self.assertEqual(params.mode, "BER")
        self.assertEqual(params["mode"], "BER")
        self.assertEqual(params.table["mode"], "BER")
        self.assertAlmostEqual(params.snrfrom, 0.00, "The Parameter class failed to parse.")
        
if __name__ == '__main__':
    unittest.main()

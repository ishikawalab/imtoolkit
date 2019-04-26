# Copyright (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt

import re

class Parameters(object):
    """description of class"""

    arg = ""
    table = {}

    # default parameters
    M = 1 # Number of transmit antennas or subcarriers
    N = 1 # Number of receive antennas
    T = 1 # Number of timeslots in a space-time codeword
    Q = 1 # Number of dispersion matrices or active indices
    P = 1 # Number of selected elements
    K = 1 # Number of selected elements
    O = 1 # Number of embedded symbols in a space-time codeword
    IT = 1 # Number of iterations
    ITo = 1 # Number of outer iterations
    ITi = 1 # Number of inner iterations
    snrfrom = 0.0 # The beginning of SNR
    to = 50.0 # The end of SNR
    len = 11 # The above SNR range is divided by len
    by = 1.0 # SNR step size
    optsnr = snr = 0.0 # A specific SNR
    sim = "coh" # Type of simulator
    channel = "rayleigh" # Channel environment
    mod = "PSK" # Type of modulation such as PAM, PSK, QAM...
    L = 2 # Number of constellation
    RC = 1 # The number of repetition
    
    # other parameters (avoid pylint errors)
    Nsc = 0 # Number of subcarriers
    Ncp = 0 # CP length
    Ns = 0 # Number of scatters in Jakes channel model
    Nt = Nr = Mt = Mr = Nu = NRF = Lc = 0
    W = R = Wl = J = PsiHalf = PhiHalf = deg = 0
    taps = mind = hit = limit = Hflu = 0

    a = d = r = v = u1 = u2 = alpha = rate = 0.0
    dTx = 0.0 # Space between source antennas or LEDs
    Rx = 0.0 # Horizontal position of a receiver
    FdTs = 0.0 # Normalized Doppler frequency in Jakes channel model
    delta = Herr = cfo = 0.0
    Kf = Dt = Dr = 0.0

    dm = "" # Type of dispersion matrices or active indices
    dec = code = Wmode = Fmode = dmi = ""
    det = basis = CR = option = ""
    minh = 0

    def __init__(self, arg):
        self.arg = arg
        
        options = arg.split("_")
        if "=" in options[0]:
            self.mode = ""
        else:
            self.mode = options.pop(0)
        self.table["mode"] = self.mode
        self.__setattr__("mode", self.mode)
        
        # parse arguments such as "M=2"
        for op in options:
            pair = op.split("=")
            pv = self.parseValue(pair[1])
            self.table[pair[0]] = pv
            self.__setattr__(pair[0], pv)
    
    #def __setattr__(self, key, value):
    #    self.table[key] = value
    #    print(self.table)
    #    return super(Parameters, self).__setattr__(key, value)

    def __getitem__(self, key):
        if key in self.table:
            return self.table[key]
        else:
            return False
        
    def parseValue(self, value):
        if re.match(r'-*\d+', value):
            if value.find("e") > 0:
                return int(float(value)) # e.g. IT=1e5, IT=2.5e7
            elif value.find(".") > 0:
                return float(value) # e.g. to=50.00
            else:
                return int(value) # e.g. M=4
        else:
            return value # e.g. channel=rayleigh

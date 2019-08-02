import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from imtoolkit import Parameters, Modulator, OSTBCode, DiagonalUnitaryCode, IdealRayleighChannel, Basis, DifferentialMLDSimulator, SemiUnitaryDifferentialMLDSimulator, NonSquareDifferentialMLDSimulator

plt.switch_backend('agg')
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['markers.fillstyle'] = 'none'

def simulateBER(argstr):
    params = Parameters(argstr)
    if params.code == "symbol":
        codes = np.array(Modulator(params.mod, params.L).symbols).reshape(params.L, 1, 1)
    elif params.code == "OSTBC":
        codes = OSTBCode(params.M, params.mod, params.L).codes
    elif params.code == "DUC":
        codes = DiagonalUnitaryCode(params.M, params.L).codes

    if params.mode == "BER":
        channel = IdealRayleighChannel(1, params.M, params.N)
    else:
        channel = IdealRayleighChannel(params.ITi, params.M, params.N)

    if params.sim == "diff":
        sim = DifferentialMLDSimulator(codes, channel)
    elif params.sim == "sudiff":
        sim = SemiUnitaryDifferentialMLDSimulator(codes, channel)
    elif params.sim == "nsdiff":
        bases = Basis(params.basis, params.M, params.T).bases
        sim = NonSquareDifferentialMLDSimulator(codes, channel, bases)

    if params.mode == "BER":
        return sim.simulateBERReference(params, outputFile=False, printValue=False)
    else:
        return sim.simulateBERParallel(params, outputFile=False, printValue=False)

if __name__ == '__main__':
    fig, ax = plt.subplots()
    ax.set_xlabel("SNR [dB]")
    ax.set_ylabel("BER")
    ax.set_xlim(0, 30)
    plt.ylim(1e-7, 1e0)
    plt.yscale("log")
    ax.tick_params(pad=8)

    ret = simulateBER("BERP_sim=sudiff_channel=rayleigh_code=symbol_M=1_N=4_L=16_mod=SQAM_ITo=1e3_ITi=1e5_snrfrom=0.00_to=30.00_len=16")
    ax.plot(ret["snr_dB"], ret["ber"], color="k", marker="s", linestyle="-", label="Differential SQAM [1]")

    os.environ['USECUPY'] = "0"
    ret = simulateBER("BER_sim=diff_channel=rayleigh_code=DUC_M=4_N=4_T=4_L=65536_IT=1e5_snrfrom=0.00_to=30.00_len=16")
    ax.plot(ret["snr_dB"], ret["ber"], color="b", marker="o", linestyle="-", label="Square DUC [2]")
    os.environ['USECUPY'] = "1"

    ret = simulateBER("BERP_sim=nsdiff_channel=rayleigh_code=DUC_basis=d_M=4_N=4_T=1_L=16_W=80_ITo=1e3_ITi=1e4_snrfrom=0.00_to=30.00_len=16")
    ax.plot(ret["snr_dB"], ret["ber"], color="r", marker="^", linestyle="-", label="Nonsquare DUC [4]")

    handles, labels = ax.get_legend_handles_labels()
    legend = ax.legend(handles, labels, loc="best", frameon=True)
    frame = legend.get_frame()
    frame.set_facecolor('white')
    frame.set_edgecolor('white')

    #plt.show()
    plt.savefig(sys.argv[0].replace(".py", ".svg"))

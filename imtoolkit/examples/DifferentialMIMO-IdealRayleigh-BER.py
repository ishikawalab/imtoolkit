import sys
import numpy as np
import matplotlib.pyplot as plt
from imtoolkit import Parameters, Modulator, OSTBCode, DiagonalUnitaryCode, ADSMCode, TASTCode, IdealRayleighChannel, DifferentialMLDSimulator

plt.switch_backend('agg')
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['markers.fillstyle'] = 'none'

def simulateBER(argstr):
    params = Parameters(argstr)
    if params.code == "symbol":
        codes = np.array(Modulator("PSK", params.L).symbols).reshape(params.L, 1, 1)
    elif params.code == "OSTBC":
        codes = OSTBCode(params.M, "PSK", params.L).codes
    elif params.code == "DUC":
        codes = DiagonalUnitaryCode(params.M, params.L).codes
    elif params.code == "ADSM":
        codes = ADSMCode(params.M, params.mod, params.L).codes
    elif params.code == "TAST":
        codes = TASTCode(params.M, params.Q, params.L).codes

    channel = IdealRayleighChannel(params.ITi, params.M, params.N)
    sim = DifferentialMLDSimulator(codes, channel)
    return sim.simulateBERParallel(params, outputFile=False, printValue=False)

if __name__ == '__main__':
    fig, ax = plt.subplots()
    ax.set_xlabel("SNR [dB]")
    ax.set_ylabel("BER")
    ax.set_xlim(-10, 30)
    plt.ylim(1e-7, 1e0)
    plt.yscale("log")
    ax.tick_params(pad=8)

    ret = simulateBER("BERP_sim=diff_channel=rayleigh_code=symbol_M=1_N=2_T=1_L=2_mod=PSK_ITo=1e3_ITi=1e5_snrfrom=-10.00_to=30.00_len=21")
    ax.plot(ret["snr_dB"], ret["ber"], color="k", marker="s", linestyle="-", label="DBPSK")

    ret = simulateBER("BERP_sim=diff_channel=rayleigh_code=OSTBC_M=2_N=2_T=2_L=2_mod=PSK_ITo=1e3_ITi=1e5_snrfrom=-10.00_to=30.00_len=21")
    ax.plot(ret["snr_dB"], ret["ber"], color="b", marker="o", linestyle="-", label="DOSTBC [1]")

    ret = simulateBER("BERP_sim=diff_channel=rayleigh_code=DUC_M=2_N=2_T=2_L=4_ITo=1e3_ITi=1e5_snrfrom=-10.00_to=30.00_len=21")
    ax.plot(ret["snr_dB"], ret["ber"], color="b", marker="^", linestyle="-", label="DUC [2]")

    ret = simulateBER("BERP_sim=diff_channel=rayleigh_code=ADSM_M=2_N=2_T=2_L=2_mod=PSK_ITo=1e3_ITi=1e5_snrfrom=-10.00_to=30.00_len=21")
    ax.plot(ret["snr_dB"], ret["ber"], color="r", marker="x", linestyle="-", label="ADSM [4]")

    ret = simulateBER("BERP_sim=diff_channel=rayleigh_code=TAST_M=2_Q=1_N=2_T=2_L=2_mod=PSK_ITo=1e3_ITi=1e5_snrfrom=-10.00_to=30.00_len=21")
    ax.plot(ret["snr_dB"], ret["ber"], color="r", marker="+", linestyle="-", label="DTAST [5]")

    handles, labels = ax.get_legend_handles_labels()
    legend = ax.legend(handles, labels, loc="best", frameon=True)
    frame = legend.get_frame()
    frame.set_facecolor('white')
    frame.set_edgecolor('white')

    #plt.show()
    plt.savefig(sys.argv[0].replace(".py", ".svg"))

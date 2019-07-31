import sys
import matplotlib.pyplot as plt
from imtoolkit import Parameters, IMCode, IdealOFDMChannel, CoherentMLDSimulator

plt.switch_backend('agg')
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['markers.fillstyle'] = 'none'

def simulateBER(argstr):
    params = Parameters(argstr)
    code = IMCode(params.dm, params.M, params.K, params.Q, params.mod, params.L, meanPower=params.M)
    channel = IdealOFDMChannel(params.ITi, params.M)
    sim = CoherentMLDSimulator(code.codes, channel)
    return sim.simulateBERParallel(params, outputFile=False, printValue=False)

if __name__ == '__main__':
    fig, ax = plt.subplots()
    ax.set_xlabel("SNR [dB]")
    ax.set_ylabel("BER")
    ax.set_xlim(-10, 40)
    plt.ylim(1e-7, 1e0)
    plt.yscale("log")
    ax.tick_params(pad=8)

    ret = simulateBER("BERP_sim=coh_code=index_dm=dic_M=16_K=8_Q=16_L=1_mod=PSK_N=16_ITo=1e3_ITi=1e4_snrfrom=-10.00_to=40.00_len=26")
    ax.plot(ret["snr_dB"], ret["ber"], color="k", marker="s", linestyle="-", label="Combinatorial design [2]")

    ret = simulateBER("BERP_sim=coh_code=index_dm=wen_M=16_K=8_Q=16_L=1_mod=PSK_N=16_ITo=1e3_ITi=1e4_snrfrom=-10.00_to=40.00_len=26")
    ax.plot(ret["snr_dB"], ret["ber"], color="b", marker="o", linestyle="-", label="Equiprobable design [3]")

    ret = simulateBER("BERP_sim=coh_code=index_dm=opt_M=16_K=8_Q=16_L=1_mod=PSK_N=16_ITo=1e3_ITi=1e4_snrfrom=-10.00_to=40.00_len=26")
    ax.plot(ret["snr_dB"], ret["ber"], color="r", marker="^", linestyle="-", label="ILP design [6]")

    handles, labels = ax.get_legend_handles_labels()
    legend = ax.legend(handles, labels, loc="best", frameon=True)
    frame = legend.get_frame()
    frame.set_facecolor('white')
    frame.set_edgecolor('white')

    #plt.show()
    plt.savefig(sys.argv[0].replace(".py", ".svg"))

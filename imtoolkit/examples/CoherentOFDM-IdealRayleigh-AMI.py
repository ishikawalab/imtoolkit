import sys
import matplotlib.pyplot as plt
from imtoolkit import Parameters, IMCode, IdealOFDMChannel, CoherentMLDSimulator

plt.switch_backend('agg')
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['markers.fillstyle'] = 'none'

def simulateAMI(argstr):
    params = Parameters(argstr)
    code = IMCode(params.dm, params.M, params.K, params.Q, params.mod, params.L, meanPower=1)
    channel = IdealOFDMChannel(params.ITi, params.M)
    sim = CoherentMLDSimulator(code.codes, channel)
    return sim.simulateAMIParallel(params, outputFile=False, printValue=False)

if __name__ == '__main__':
    fig, ax = plt.subplots()
    ax.set_xlabel("SNR [dB]")
    ax.set_ylabel("AMI [bps/Hz]")
    ax.set_xlim(-20, 30)
    ax.set_ylim(0, 1)
    ax.tick_params(pad = 8)

    ret = simulateAMI("AMIP_sim=coh_code=index_dm=dic_M=4_K=4_Q=1_L=2_mod=PSK_N=4_ITo=1_ITi=1e4_snrfrom=-20.00_to=30.00_len=26")
    ax.plot(ret["snr_dB"], ret["ami"]/4, color="k", marker="s", linestyle="-", label="OFDM")

    ret = simulateAMI("AMIP_sim=coh_code=index_dm=opt_M=4_K=1_Q=4_L=4_mod=PSK_N=4_ITo=1_ITi=1e4_snrfrom=-20.00_to=30.00_len=26")
    ax.plot(ret["snr_dB"], ret["ami"]/4, color="r", marker="o", linestyle="-", label="Subcarrier-index modulation")

    handles, labels = ax.get_legend_handles_labels()
    legend = ax.legend(handles, labels, loc="best", frameon=True)
    frame = legend.get_frame()
    frame.set_facecolor('white')
    frame.set_edgecolor('white')

    #plt.show()
    plt.savefig(sys.argv[0].replace(".py", ".svg"))

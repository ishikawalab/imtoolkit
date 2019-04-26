========
Tutorial
========

This webpage introduces a detailed tutorial for the ``imtoolkit`` command, which can be installed by ``pip install imtoolkit``.


Basic Usage
===========

The command line option is specified by a sentence concatenated by underscores.

.. code-block:: bash

    > imtoolkit {MODE}_code=index_dm={dic,wen,opt}_ + other parameters

Here, the CuPy-aided operation is enabled by setting an environment variable ``USECUPY=1`` before executing ``imtoolkit``.

.. code-block:: bash

    > export USECUPY=1

In case you would like to use Numpy, please unset the environment variable.

.. code-block:: bash

    > unset USECUPY

Usage Examples
===============

Check the transmission rate of the IM codebook having :math:`(M,K,Q)=(2,1,2)` and BPSK constellation.

.. code-block:: bash

    > imtoolkit RATE_code=index_dm=dic_M=2_K=1_Q=2_L=2_mod=PSK
    B = B1 + B2 = 1 + 1 = 2 [bits/symbol]

Check the IM codebooks having various parameters.

.. code-block:: bash

    > imtoolkit VIEW_code=index_dm=dic_M=2_K=1_Q=2_L=2_mod=PSK
    > imtoolkit VIEW_code=index_dm=wen_M=16_K=8_Q=16_L=1_mod=PSK
    > imtoolkit VIEW_code=index_dm=opt_M=16_K=8_Q=16_L=1_mod=PSK

Check the active indeces having :math:`(M,K,Q)=(16,8,16)`.

.. code-block:: bash

    > imtoolkit VIEWIM_code=index_dm=opt_M=16_K=8_Q=16
    [[1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0]
     [1 1 1 1 0 0 0 0 1 1 1 1 0 0 0 0]
     [1 1 1 1 0 0 0 0 0 0 0 0 1 1 1 1]
     [1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0]
     [1 1 0 0 1 1 0 0 0 0 1 1 0 0 1 1]
     [1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0]
     [1 0 0 1 0 1 1 0 1 0 0 1 0 1 1 0]
     [1 0 0 1 0 1 1 0 0 1 1 0 1 0 0 1]
     [0 1 1 0 1 0 0 1 1 0 0 1 0 1 1 0]
     [0 1 1 0 1 0 0 1 0 1 1 0 1 0 0 1]
     [0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1]
     [0 0 1 1 0 0 1 1 1 1 0 0 1 1 0 0]
     [0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1]
     [0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0]
     [0 0 0 0 1 1 1 1 0 0 0 0 1 1 1 1]
     [0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1]]
    Minimum Hamming distance = 8
    Inequality L1 = 0

Check the minimum Euclidean distance of the IM codebook having :math:`(M,K,Q)=(2,1,2)` and BPSK constellation.

.. code-block:: bash

    > imtoolkit MED_channel=rayleigh_code=index_dm=dic_M=2_K=1_Q=2_L=2_mod=PSK
    export USECUPY=1
    MED = 2.0000000000000004

Check the BER of the BLAST scheme having BPSK constellation over the ideal Rayleigh fading channel.

.. code-block:: bash

    > imtoolkit BER_sim=coh_channel=rayleigh_code=index_dm=dic_M=2_K=2_Q=1_L=2_mod=PSK_N=1_IT=1e6_snrfrom=0.00_to=50.00_len=11
    > imtoolkit BERP_sim=coh_channel=rayleigh_code=index_dm=dic_M=2_K=2_Q=1_L=2_mod=PSK_N=1_ITo=1e2_ITi=1e4_snrfrom=0.00_to=50.00_len=11
    At SNR = 0.00 dB, BER = 286270 / 1200000 = 0.23855833333333334445
    At SNR = 5.00 dB, BER = 165053 / 1200000 = 0.13754416666666666180
    At SNR = 10.00 dB, BER = 72774 / 1200000 = 0.06064499999999999752
    At SNR = 15.00 dB, BER = 26499 / 1200000 = 0.02208250000000000143
    At SNR = 20.00 dB, BER = 8899 / 1200000 = 0.00741583333333333330
    At SNR = 25.00 dB, BER = 2810 / 1200000 = 0.00234166666666666681
    At SNR = 30.00 dB, BER = 861 / 1200000 = 0.00071750000000000004
    At SNR = 35.00 dB, BER = 274 / 1200000 = 0.00022833333333333334
    At SNR = 40.00 dB, BER = 74 / 1200000 = 0.00006166666666666667
    At SNR = 45.00 dB, BER = 28 / 1200000 = 0.00002333333333333333
    At SNR = 50.00 dB, BER = 10 / 1200000 = 0.00000833333333333333
     15%|████████▎                                              | 15/100 [00:03<00:21,  3.87it/s]

Check the BER of the spatial modulation scheme over the ideal Rayleigh fading channel.

.. code-block:: bash

    > imtoolkit BER_sim=coh_channel=rayleigh_code=index_dm=dic_M=2_K=1_Q=2_L=2_mod=PSK_N=1_IT=1e6_snrfrom=0.00_to=50.00_len=11
    > imtoolkit BERP_sim=coh_channel=rayleigh_code=index_dm=dic_M=2_K=1_Q=2_L=2_mod=PSK_N=1_ITo=1e2_ITi=1e4_snrfrom=0.00_to=50.00_len=11

Similarly, check the AMI of the above setup.

.. code-block:: bash

    > imtoolkit AMI_sim=coh_channel=rayleigh_code=index_dm=dic_M=2_K=1_Q=2_L=2_mod=PSK_N=1_IT=1e4_snrfrom=-20.00_to=30.00_len=11
    > imtoolkit AMIP_sim=coh_channel=rayleigh_code=index_dm=dic_M=2_K=1_Q=2_L=2_mod=PSK_N=1_ITo=1e1_ITi=1e3_snrfrom=-20.00_to=30.00_len=11

Check the BER and AMI of the subcarrier index modulation scheme over the ideal frequency-selective OFDM channel.

.. code-block:: bash

    > imtoolkit BER_sim=coh_channel=ofdm_code=index_dm=dic_M=2_K=1_Q=2_L=2_mod=PSK_IT=1e6_snrfrom=0.00_to=50.00_len=11
    > imtoolkit BERP_sim=coh_channel=ofdm_code=index_dm=dic_M=2_K=1_Q=2_L=2_mod=PSK_ITo=1e2_ITi=1e4_snrfrom=0.00_to=50.00_len=11
    > imtoolkit AMI_sim=coh_channel=ofdm_code=index_dm=dic_M=2_K=1_Q=2_L=2_mod=PSK_IT=1e5_snrfrom=-20.00_to=30.00_len=11
    > imtoolkit AMIP_sim=coh_channel=ofdm_code=index_dm=dic_M=2_K=1_Q=2_L=2_mod=PSK_ITo=1e1_ITi=1e4_snrfrom=-20.00_to=30.00_len=11
    At SNR = -20.00 dB, AMI = 0.02835752386965842420
    At SNR = -15.00 dB, AMI = 0.08621969236346302412
    At SNR = -10.00 dB, AMI = 0.24553548125900576116
    At SNR = -5.00 dB, AMI = 0.61030449159960853400
    At SNR = 0.00 dB, AMI = 1.19762564984552777325
    At SNR = 5.00 dB, AMI = 1.71401898627954807353
    At SNR = 10.00 dB, AMI = 1.92946990000208695726
    At SNR = 15.00 dB, AMI = 1.98357959973452779856
    At SNR = 20.00 dB, AMI = 1.99521501735232775765
    At SNR = 25.00 dB, AMI = 1.99846647081199679796
    At SNR = 30.00 dB, AMI = 1.99952712587336933758
     80%|████████████████████████████████████████████████████████████████████████████████                    | 8/10 [00:03<00:00,  2.24it/s]





Parameters
==========

The execution mode can be switched by the first argument ``MODE``.


MODE
    RATE
        Check the transmission rate [bits/symbol]. Please remind that we need to divide it by ``M`` for the SIM case.
    MED
        Check the minimum Eunclidean distance of the specified codebook, which correlates with the achievable performance.
    BER
        Execute bit error rate (BER) simulatoins for multiple SNRs, where the straightforward reference algorithm is used.
    BERP
        Execute BER simulatoins for multiple SNRs, where the massively parallel algorithm is used. 
    AMI
        Execute average mutual information (AMI) simulatoins for multiple SNRs, where the straightforward reference algorithm is used.
    AMIP
        Execute AMI simulatoins for multiple SNRs, where the massively parallel algorithm is used. 
    VIEW
        Print the specified codebook.
    VIEWIM
        Print the specified active indices.
    VIEWIMTEX
        Print the specified active indices in a tex format.
sim
    coh
        IMToolkit currently supports the coherent maximum likelihood detection only.
channel
    rayleigh
        Use the ideal Rayleigh fading channel, which is generated by the complex Gaussian distribution.
    ofdm
        Use the ideal OFDM channel, which is generated by diagonal matrices.
code
    index
        IMToolkit currently supports the IM codebook only. But, ``M=K`` setup is equivalent to the conventional BLAST or OFDM signaling.
dm
    dic
        Use the combinatorial design for active indices.
    wen
        Use the equiprobable design for active indices.
    opt
        Use the theoretical optimal design for active indices.
M
    Number of transmit antennas or subcarriers.
N
    Number of receive antennas.
Q
    Number of active indices.
K
    Number of selected antennas or subcarriers.
mod
    PSK
        Use the PSK constellation
    QAM
        Use the QAM constellation.
    SQAM
        Use the star QAM constellation.
L
    Number of constellation.
IT
    Number of iterations for the MODE = BER or AMI cases.
ITo
    Number of outer iterations
ITi
    Number of inner iterations
snrfrom
    The beginning of SNR range.
to
    The end of SNR range.
len
    The length of SNR range.



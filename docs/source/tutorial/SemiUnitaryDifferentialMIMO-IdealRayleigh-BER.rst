================================================
SemiUnitaryDifferentialMIMO-IdealRayleigh-BER.py
================================================

This webpage introduces an API example for the noncohrent scenario, which uses :doc:`SemiUnitaryDifferentialMLDSimulator <../module/imtoolkit.SemiUnitaryDifferentialMLDSimulator>`.
Other examples are found in :doc:`SemiUnitaryDifferentialMLDSimulatorTest <../module/imtoolkit.tests.SemiUnitaryDifferentialMLDSimulatorTest>`.

This example compares the BER performance of the differential star-QAM (SQAM), differential orthogonal space-time block code (DOSTBC) with SQAM, and diagonal unitary code (DUC) schemes.
The simulation parameters are given in the table below.

Performance Results
===================

.. image:: ../../../imtoolkit/examples/SemiUnitaryDifferentialMIMO-IdealRayleigh-BER.svg
   :align: center

Simulation Parameters
=====================

+-----------------------------+----------------------------------+
| Parameter                   | Value                            |
+=============================+==================================+
| Channel                     | Ideal Rayleigh fading            |
+-----------------------------+----------------------------------+
| Number of transmit antennas | :math:`M=2`                      |
+-----------------------------+----------------------------------+
| Number of receive antennas  | :math:`N=2`                      |
+-----------------------------+----------------------------------+
| Constellation size          | :math:`L=16,256`                 |
+-----------------------------+----------------------------------+
| Transmission rate           | :math:`R=B/T=8/2=4` [bit/symbol] |
+-----------------------------+----------------------------------+

Reproducible Code
=================

.. literalinclude:: ../../../imtoolkit/examples/SemiUnitaryDifferentialMIMO-IdealRayleigh-BER.py
   :language: python

Related Publications
====================
- [1] W. T. Webb, L. Hanzo, and R. Steele, "`Bandwidth efficient QAM schemes for Rayleigh fading channels <https://ieeexplore.ieee.org/document/98701>`_," IEE Proc., vol. 138, no. 3, pp. 169--175, 1991.

- [2] S. Alamouti, "`A simple transmit diversity technique for wireless communications <https://doi.org/10.1109/49.730453>`_," IEEE J. Sel. Areas Commun., vol. 16, no. 8, pp. 1451--1458, 1998.

- [3] B. M. Hochwald and W. Sweldens, "`Differential unitary space-time modulation <https://doi.org/10.1109/26.891215>`_," IEEE Trans. Commun., vol. 48, no. 12, pp. 2041--2052, 2000.

- [4] N. Ishikawa, "`IMToolkit: An open-source index modulation toolkit for reproducible research based on massively parallel algorithms <https://doi.org/10.1109%2Faccess.2019.2928033>`_," IEEE Access, vol. 7, pp. 93830--93846, July 2019.


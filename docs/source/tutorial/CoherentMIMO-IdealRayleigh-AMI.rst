=================================
CoherentMIMO-IdealRayleigh-AMI.py
=================================

This webpage introduces an API example for the cohrent scenario, which uses :doc:`CoherentMLDSimulator. <../module/imtoolkit.CoherentMLDSimulator>`.
Other examples are found in :doc:`CoherentMLDSimulatorTest <../module/imtoolkit.tests.CoherentMLDSimulatorTest>`.

This example compares the AMI performance of the coherent BLAST and spatial modulation schemes, where the simulation parameters are given in the table below.

Performance Results
===================

.. image:: ../../../imtoolkit/examples/CoherentMIMO-IdealRayleigh-AMI.svg
   :align: center

Simulation Parameters
=====================

+-----------------------------+--------------------------+
| Parameter                   | Value                    |
+=============================+==========================+
| Channel                     | Ideal Rayleigh fading    |
+-----------------------------+--------------------------+
| Number of transmit antennas | :math:`M=4`              |
+-----------------------------+--------------------------+
| Number of receive antennas  | :math:`N=4`              |
+-----------------------------+--------------------------+
| Constellation size          | :math:`L=2,4`            |
+-----------------------------+--------------------------+
| Transmission rate           | :math:`R=4` [bit/symbol] |
+-----------------------------+--------------------------+

Reproducible Code
=================

.. literalinclude:: ../../../imtoolkit/examples/CoherentMIMO-IdealRayleigh-AMI.py
   :language: python

Related Publications
====================
- [1] R. Y. Mesleh, H. Haas, S. Sinanovic, C. W. Ahn, and S. Yun, "`Spatial modulation <https://doi.org/10.1109/TVT.2007.912136>`_," IEEE Trans. Veh. Technol., vol. 57, no. 4, pp. 2228--2241, 2008.

- [2] R. Mesleh and A. Alhassi, `Space modulation techniques <https://onlinelibrary.wiley.com/doi/book/10.1002/9781119375692>`_. Wiley, 2018.

- [3] N. Ishikawa, S. Sugiura, and L. Hanzo, "`50 years of permutation, spatial and index modulation: From classic RF to visible light communications and data storage <https://doi.org/10.1109/COMST.2018.2815642>`_," IEEE Commun. Surv. Tutorials, vol. 20, no. 3, pp. 1905--1938, 2018.

- [4] N. Ishikawa, "`IMToolkit: An open-source index modulation toolkit for reproducible research based on massively parallel algorithms <https://doi.org/10.1109%2Faccess.2019.2928033>`_," IEEE Access, vol. 7, pp. 93830--93846, July 2019.

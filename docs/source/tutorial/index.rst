========
Tutorial
========

This webpage introduces a detailed tutorial for the ``imtoolkit`` command and APIs.
The ``imtoolkit`` command is a stand-alone toolkit for the spatial modulation and subcarrier-index modulation schemes, which supports Windows, Mac, and Linux.
By contrast, the ``imtoolkit`` APIs provide various classes and functions for the general MIMO/OFDM scenarios.

Before using ``imtoolkit``, one can activate the CuPy-aided GPGPU acceleration by setting an environment variable ``USECUPY=1`` as follows.

.. code-block:: bash

    > export USECUPY=1

In case you would like to use the CPU backend, NumPy, please unset the environment variable.

.. code-block:: bash

    > unset USECUPY

.. toctree::
   :maxdepth: 2
   :hidden:

   imtoolkit-command
   CoherentMIMO-IdealRayleigh-BER
   CoherentMIMO-IdealRayleigh-AMI
   CoherentOFDM-IdealRayleigh-BER
   CoherentOFDM-IdealRayleigh-BER-diversity
   CoherentOFDM-IdealRayleigh-AMI
   DifferentialMIMO-IdealRayleigh-BER
   SemiUnitaryDifferentialMIMO-IdealRayleigh-BER
   NonSquareDifferentialMIMO-IdealRayleigh-BER

.. raw:: html

   <h2>How to use the imtoolkit command</h2>

- :doc:`Tutorial for the installed imtoolkit command. <imtoolkit-command>`

.. raw:: html

   <h2>API examples for the imtoolkit package</h2>

.. image:: ../../../imtoolkit/examples/CoherentMIMO-IdealRayleigh-BER.svg
   :align: right
   :width: 150px
   :target: CoherentMIMO-IdealRayleigh-BER.html

- :doc:`CoherentMIMO-IdealRayleigh-BER.py <CoherentMIMO-IdealRayleigh-BER>`

    - This example compares the BER performance of the coherent Bell laboratories layered space-time (BLAST) and spatial modulation (SM) schemes.

.. raw:: html

   <br clear="all">


.. image:: ../../../imtoolkit/examples/CoherentMIMO-IdealRayleigh-AMI.svg
   :align: right
   :width: 150px
   :target: CoherentMIMO-IdealRayleigh-AMI.html

- :doc:`CoherentMIMO-IdealRayleigh-AMI.py <CoherentMIMO-IdealRayleigh-AMI>`

    - This example compares the AMI performance of the coherent BLAST and SM schemes.

.. raw:: html

   <br clear="all">


.. image:: ../../../imtoolkit/examples/CoherentOFDM-IdealRayleigh-BER.svg
   :align: right
   :width: 150px
   :target: CoherentOFDM-IdealRayleigh-BER.html

- :doc:`CoherentOFDM-IdealRayleigh-BER.py <CoherentOFDM-IdealRayleigh-BER>`

    - This example compares the BER performance of the coherent OFDM and subcarrier-index modulation (SIM) schemes.

.. raw:: html

   <br clear="all">


.. image:: ../../../imtoolkit/examples/CoherentOFDM-IdealRayleigh-BER-diversity.svg
   :align: right
   :width: 150px
   :target: CoherentOFDM-IdealRayleigh-BER-diversity.html

- :doc:`CoherentOFDM-IdealRayleigh-BER-diversity.py <CoherentOFDM-IdealRayleigh-BER-diversity>`

    - This example evaluates the BER performance of the coherent SIM scheme, where three subcarrier activation patterns are considered.

.. raw:: html

   <br clear="all">


.. image:: ../../../imtoolkit/examples/CoherentOFDM-IdealRayleigh-AMI.svg
   :align: right
   :width: 150px
   :target: CoherentOFDM-IdealRayleigh-AMI.html

- :doc:`CoherentOFDM-IdealRayleigh-AMI.py <CoherentOFDM-IdealRayleigh-AMI>`

    - This example compares the AMI performance of the coherent OFDM and SIM schemes.

.. raw:: html

   <br clear="all">


.. image:: ../../../imtoolkit/examples/DifferentialMIMO-IdealRayleigh-BER.svg
   :align: right
   :width: 150px
   :target: DifferentialMIMO-IdealRayleigh-BER.html

- :doc:`DifferentialMIMO-IdealRayleigh-BER.py <DifferentialMIMO-IdealRayleigh-BER>`

    - This example compares the BER performance of the differential BPSK, differential orthogonal space-time block code (DOSTBC), diagonal unitary code (DUC), algebraic differential spatial modulation (ADSM), and differential threaded algebraic space-time (DTAST) schemes.

.. raw:: html

   <br clear="all">

.. image:: ../../../imtoolkit/examples/SemiUnitaryDifferentialMIMO-IdealRayleigh-BER.svg
   :align: right
   :width: 150px
   :target: SemiUnitaryDifferentialMIMO-IdealRayleigh-BER.html

- :doc:`SemiUnitaryDifferentialMIMO-IdealRayleigh-BER.py <SemiUnitaryDifferentialMIMO-IdealRayleigh-BER>`

    - This example compares the BER performance of the differential star-QAM (SQAM), DOSTBC with SQAM, and DUC schemes.

.. raw:: html

   <br clear="all">

.. image:: ../../../imtoolkit/examples/NonSquareDifferentialMIMO-IdealRayleigh-BER.svg
   :align: right
   :width: 150px
   :target: NonSquareDifferentialMIMO-IdealRayleigh-BER.html

- :doc:`NonSquareDifferentialMIMO-IdealRayleigh-BER.py <NonSquareDifferentialMIMO-IdealRayleigh-BER>`

    - This example compares the BER performance of the differential SQAM, square DUC, and nonsquare DUC schemes.

.. raw:: html

   <br clear="all">

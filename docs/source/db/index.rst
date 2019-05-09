=======================
Active Indices Database
=======================

This webpage introduces a comprehensive database of the active indices designed for the generalized spatial modulation and the subcarrier index modulation schemes, which are representative members of index modulation family.
The designed active indices are provided in three formats: pure indices, activation tensor, and its vector representation.
Note that the activation tensor is omitted for the :math:`Q \cdot M \cdot K > 10^6` case.
Additionally, the designed active indices having :math:`M > 32` are omitted due to their large file size, but are supported by the IMToolkit search algorithm.

.. csv-table::
   :header: , Coverage
   :widths: 5, 5

   :math:`M \leq 16`, 100%


.. toctree::
   :maxdepth: 2
   :hidden:
   
   M=2/index
   M=4/index
   M=6/index
   M=8/index
   M=10/index
   M=12/index
   M=14/index
   M=16/index
   M=18/index
   M=20/index
   M=22/index
   M=24/index
   M=26/index
   M=28/index
   M=30/index
   M=32/index

:doc:`M=2/index` / :doc:`M=4/index` / :doc:`M=6/index` / :doc:`M=8/index` / :doc:`M=10/index` / :doc:`M=12/index` / :doc:`M=14/index` / :doc:`M=16/index` / :doc:`M=18/index` / :doc:`M=20/index` / :doc:`M=22/index` / :doc:`M=24/index` / :doc:`M=26/index` / :doc:`M=28/index` / :doc:`M=30/index` / :doc:`M=32/index`

The active indices can be also obtained by the ``VIEWIM`` mode.
For example, for the :math:`(M,K,Q)=(16,8,16)` case, the corresponding active indices are obtained by executing the following command.

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


.. imtoolkit\docs\source\library>imsearch VIEWH_M=6 > "M=6.rst"


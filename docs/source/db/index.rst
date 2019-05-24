=======================
Active Indices Database
=======================

This webpage introduces a comprehensive database of the active indices designed for the generalized spatial modulation and the subcarrier index modulation schemes, which are representative members of index modulation family.
The designed active indices are provided in three formats: pure indices, activation tensor, and its vector representation.
Note that the designed active indices for the :math:`Q > 1024` case are omitted in this webpage, although they are supported by this toolkit.
Additionally, the activation tensor is omitted for the :math:`Q > 128` case due to its large file size.

:doc:`M=2/index` / :doc:`M=4/index` / :doc:`M=6/index` / :doc:`M=8/index` / :doc:`M=10/index` / :doc:`M=12/index` / :doc:`M=14/index` / :doc:`M=16/index` / :doc:`M=18/index` / :doc:`M=20/index` / :doc:`M=22/index` / :doc:`M=24/index` / :doc:`M=26/index` / :doc:`M=28/index` / :doc:`M=30/index` / :doc:`M=32/index`

The following table summarizes the coverage for IM parameter set :math:`(M, K, Q)`.
As shown in this table, all of the IM parameters are perfectly supported for the :math:`M \leq 16` case.
.. csv-table::
   :header: , Coverage
   :widths: 5, 5

   :math:`M \leq 16`, 100.00%
   :math:`M \leq 20`, 99.67%
   :math:`M \leq 24`, 99.04%
   :math:`M \leq 28`, 89.93%
   :math:`M \leq 32`, 72.14%
.. imsearch COVERAGE

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

One can also obtain the designed active indices by the ``VIEWIM`` mode.
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


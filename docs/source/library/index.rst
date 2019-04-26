======================
Active Indices Library
======================

This webpage introduces a comprehensive library of the active indices designed for the generalized spatial modulation and the subcarrier index modulation schemes, which are representative members of index modulation family.
Here, the designed active indices having :math:`M > 12` are omitted due to their large file size, but are supported by IMToolkit.

.. toctree::
   :maxdepth: 2
   :hidden:
   
   M=2
   M=4
   M=6
   M=8
   M=10
   M=12

:doc:`M=2` / :doc:`M=4` / :doc:`M=6` / :doc:`M=8` / :doc:`M=10` / :doc:`M=12`

The active indices for the :math:`M > 12` case can be obtained by the ``VIEWIM`` mode.
For example, for the :math:`(M,K,Q)=(16,8,16)` case, the corresponding active indices are given below.

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


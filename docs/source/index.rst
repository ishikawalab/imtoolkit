.. imtoolkit documentation master file, created by
   sphinx-quickstart on Tue Apr 23 15:53:04 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=========
Overview
=========

This webpage introduces an open-source index modulation toolkit (IMToolkit).
This toolkit attempts to enable reproducible research in the field of wireless communications and IM studies.
It contains massively parallel algorithms for Monte-Carlo simulations, which are especially designed for Nvidia GPUs.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:

   self
   tutorial
   library/index

Installation Guide
==================

IMToolkit is available from the Python official package repository `PyPi <https://pypi.org/project/imtoolkit/>`_.

.. code-block:: bash

    > pip install imtoolkit

This installation requires Numba, NumPy, Pandas, SciPy, SymPy, and tqdm, all of which are popular Python packages.
Additionally, it is strongly recommended to install `CuPy <https://cupy.chainer.org/>`_ 5.40+. 
IMToolkit is heavily dependent on CuPy to achieve significantly fast Monte-Carlo simulations.
`The key components required by CuPy are listed here. <https://docs-cupy.chainer.org/en/stable/install.html>`_
In case CuPy is not installed in your environment, IMToolkit uses NumPy only.
Note that the CuPy-based ideal simulation is 145 times faster than this NumPy-based calculation, as reported in [1].

The latest development version is also available from `GitHub <https://github.com/imtoolkit/imtoolkit>`_.

.. code-block:: bash

    > pip install git+https://github.com/imtoolkit/imtoolkit

The IMToolkit development team is welcome to incorporate other researchers contributions and pull requests.

How to Use
==========
- :doc:`A detailed tutorial for the installed imtoolkit command. <tutorial>`
- :doc:`A comprehensive library of the designed active indices. <library/index>`

Citations
=========
It would be very appreciated if you cite the following references when using IMToolkit.

 [1] N. Ishikawa, "IMToolkit: An open-source index modulation toolkit for reproducible research based on massively parallel algorithms," IEEE Access, submitted.

Of course, if your project relies on CuPy, the following reference is highly recommended.

 [2] R. Okuta, Y. Unno, D. Nishino, S. Hido, and C. Loomis, "CuPy: A numPy-compatible library for NVIDIA GPU calculations," in Conference on Neural Information Processing Systems Workshop, Long Beach, CA, USA, Dec. 4-9, 2017.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

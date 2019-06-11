# IMToolkit

IMToolkit, an open-source index modulation (IM) toolkit, attempts to facilitate reproducible research in the field of wireless communications and IM studies.
The major advantages of this toolkit are highlighted as follows:

- With the aid of state-of-the-art Nvidia GPUs, it accelerates bit error ratio and average mutual information simulations by invoking massively parallel algorithms.
- In addition to the IM family, it also supports the conventional multiplexing scheme for ideal MIMO and OFDM scenarios.
- It contains a comprehensive database of designed active indices, that determine the achievable performance of the generalized spatial modulation or the subcarrier-index modulation.

For more information, please refer to the following webpages.
- [IMToolkit official website](https://ishikawa.cc/imtoolkit/)
- [A detailed tutorial for the imtoolkit command](https://ishikawa.cc/imtoolkit/tutorial.html)
- [A comprehensive database of the designed active indices](https://ishikawa.cc/imtoolkit/db/index.html)

## Installation Guide

IMToolkit is available from the Python official package repository [PyPi](https://pypi.org/project/imtoolkit/).

    > pip install imtoolkit

This installation requires Numba, NumPy, Pandas, SciPy, SymPy, and tqdm, all of which are popular Python packages.
Additionally, it is strongly recommended to install [CuPy](https://cupy.chainer.org/) 5.40+. 
IMToolkit is heavily dependent on CuPy to achieve significantly fast Monte-Carlo simulations.
[The key components required by CuPy are listed here.](https://docs-cupy.chainer.org/en/stable/install.html)
In case CuPy is not installed in your environment, IMToolkit uses NumPy only.
Note that the CuPy-based simulation is 145 times faster than the NumPy-based calculation, as reported in [1].

The above package does not include the designed active indices due to their large file size, which exceeds 500MB.
Hence, the required files are automatically obtained from the GitHub repository or a mirror website.
If you need all the project files, to use `imtoolkit` offline, it is recommended to obtain the package obtained from GitHub as follows:

    > pip install git+https://github.com/imtoolkit/imtoolkit

The IMToolkit development team welcomes other researchers' contributions and pull requests.
In that case, it would be better to install the latest package as follows:

    > git clone https://github.com/imtoolkit/imtoolkit
    > pip install -e ./imtoolkit # this activates the editable mode

[A detailed tutorial for the installed imtoolkit command is available here.](https://ishikawa.cc/imtoolkit/tutorial.html)

## Citations

It would be highly appreciated if you cite the following reference when using IMToolkit.

- [1] N. Ishikawa, "IMToolkit: An open-source index modulation toolkit for reproducible research based on massively parallel algorithms," IEEE Access, submitted.

Of course, if your project relies on CuPy, the following reference is strongly recommended.

- [2] R. Okuta, Y. Unno, D. Nishino, S. Hido, and C. Loomis, "[CuPy: A numPy-compatible library for NVIDIA GPU calculations](http://learningsys.org/nips17/assets/papers/paper_16.pdf)," in Conference on Neural Information Processing Systems Workshop, Long Beach, CA, USA, Dec. 4-9, 2017.


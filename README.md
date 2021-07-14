# IMToolkit

<a href="https://github.com/ishikawalab/imtoolkit"><img align="right" width="150px" height="150px" src="https://user-images.githubusercontent.com/62990567/88035979-def26700-cb7d-11ea-99a0-db4a4c9bec30.png"></a>
IMToolkit, an open-source index modulation (IM) toolkit, attempts to facilitate reproducible research in wireless communications.
The major advantages of this toolkit are highlighted as follows:

- It accelerates bit error ratio and average mutual information simulations by relying on a state-of-the-art Nvidia GPU and the massively parallel algorithms proposed in [1].
- It also supports the representative multiplexing schemes for ideal MIMO and OFDM scenarios, in addition to the IM family.
- It contains [a comprehensive database of designed active indices](https://ishikawa.cc/imtoolkit/db/index.html), that determine the achievable performance of the generalized spatial modulation or the subcarrier-index modulation.

For more information, please refer to the following webpages.
- [IMToolkit official website](https://ishikawa.cc/imtoolkit/).
- [A detailed tutorial for the imtoolkit command](https://ishikawa.cc/imtoolkit/tutorial/index.html).
- [A comprehensive database of the designed active indices](https://ishikawa.cc/imtoolkit/db/index.html).
- [A compute capsule on Code Ocean](https://codeocean.com/capsule/4685246/tree), that reproduces the same results as those reported in [1].

## Installation Guide

IMToolkit is available from the Python official package repository [PyPi](https://pypi.org/project/imtoolkit/).

    > pip install imtoolkit

This installation requires NumPy, Pandas, SciPy, SymPy, Numba, and tqdm, all of which are popular Python packages.
Additionally, it is strongly recommended to install [CuPy](https://cupy.chainer.org/) 5.40+. 
IMToolkit is heavily dependent on CuPy to achieve significantly fast Monte Carlo simulations.
[The key components required by CuPy are listed here.](https://docs-cupy.chainer.org/en/stable/install.html)
In case CuPy is not installed in your environment, IMToolkit uses NumPy only.
Note that the CuPy-based simulation is 145 times faster than the NumPy-based calculation, as reported in [1].

[The above PyPi package](https://pypi.org/project/imtoolkit/) excluded the designed active indices due to their large file size, which exceeds 500MB.
Hence, this reduced-size PyPi package will automatically download a required file from the GitHub repository or a mirror website.
If you need all the project files, to use `imtoolkit` offline, it is recommended to obtain the whole package from GitHub as follows:

    > pip install git+https://github.com/ishikawalab/imtoolkit

The IMToolkit development team welcomes other researchers' contributions and pull requests.
In that case, it would be better to install the latest package and activate the editable mode as follows:

    > git clone https://github.com/ishikawalab/imtoolkit
    > pip install -e ./imtoolkit # this activates the editable mode

If you use Anaonda version 4.6.0 or above, the following commands will work.

    > conda config --set pip_interop_enabled True
    > # for typical users
    > pip install imtoolkit
    > # for developers
    > git clone https://github.com/ishikawalab/imtoolkit
    > pip install -e ./imtoolkit

[A detailed tutorial for the installed imtoolkit command is available here.](https://ishikawa.cc/imtoolkit/tutorial/index.html)

## Citations

It would be highly appreciated if you cite the following reference when using IMToolkit.

- [1] N. Ishikawa, ``[IMToolkit: An open-source index modulation toolkit for reproducible research based on massively parallel algorithms](https://doi.org/10.1109%2Faccess.2019.2928033),'' IEEE Access, vol. 7, pp. 93830--93846, July 2019.

Of course, if your project relies on CuPy, the following reference is strongly recommended.

- [2] R. Okuta, Y. Unno, D. Nishino, S. Hido, and C. Loomis, ``[CuPy: A NumPy-compatible library for NVIDIA GPU calculations](http://learningsys.org/nips17/assets/papers/paper_16.pdf),'' in Conference on Neural Information Processing Systems Workshop, Long Beach, CA, USA, December 4--9, 2017.

## Contributor(s)

- Naoki Ishikawa ([Web](https://ishikawa.cc) / [Google Scholar](https://scholar.google.co.jp/citations?user=JHnisGYAAAAJ) / [ResearchGate](https://www.researchgate.net/profile/Naoki_Ishikawa) / [Publons](https://publons.com/researcher/3012020/naoki-ishikawa/))
- You might become a valuable contributor of this project. Any contributions and issues are appreciated.


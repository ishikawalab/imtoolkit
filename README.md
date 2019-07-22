# IMToolkit

<a href="https://github.com/imtoolkit/imtoolkit"><img align="right" width="150px" height="150px" src="https://github.com/imtoolkit/imtoolkit/blob/master/docs/source/_static/imtoolkit-logo.png?raw=true"></a>
IMToolkit, an open-source index modulation (IM) toolkit, attempts to facilitate reproducible research in wireless communications.
The major advantages of this toolkit are highlighted as follows:

- It accelerates bit error ratio and average mutual information simulations by relying on a state-of-the-art Nvidia GPU and the massively parallel algorithms proposed in [1].
- It also supports the representative multiplexing schemes for ideal MIMO and OFDM scenarios, in addition to the IM family.
- It contains <a href="https://ishikawa.cc/imtoolkit/db/index.html" target="_blank">a comprehensive database of designed active indices</a>, that determine the achievable performance of the generalized spatial modulation or the subcarrier-index modulation.

For more information, please refer to the following webpages.
- <a href="https://ishikawa.cc/imtoolkit/" target="_blank">IMToolkit official website</a>
- <a href="https://ishikawa.cc/imtoolkit/tutorial.html" target="_blank">A detailed tutorial for the imtoolkit command</a>
- <a href="https://ishikawa.cc/imtoolkit/db/index.html" target="_blank">A comprehensive database of the designed active indices</a>
- <a href="https://codeocean.com/capsule/4685246/tree" target="_blank">A compute capsule on Code Ocean</a>

## Installation Guide

IMToolkit is available from the Python official package repository <a href="https://pypi.org/project/imtoolkit/" target="_blank">PyPi</a>.

    > pip install imtoolkit

This installation requires NumPy, Pandas, SciPy, SymPy, and tqdm, all of which are popular Python packages.
Additionally, it is strongly recommended to install <a href="https://cupy.chainer.org/" target="_blank">CuPy</a> 5.40+. 
IMToolkit is heavily dependent on CuPy to achieve significantly fast Monte Carlo simulations.
<a href="https://docs-cupy.chainer.org/en/stable/install.html" target="_blank">The key components required by CuPy are listed here.</a>
In case CuPy is not installed in your environment, IMToolkit uses NumPy only.
Note that the CuPy-based simulation is 145 times faster than the NumPy-based calculation, as reported in [1].

<a href="https://pypi.org/project/imtoolkit/" target="_blank">The above PyPi package</a> excluded the designed active indices due to their large file size, which exceeds 500MB.
Hence, this reduced-size PyPi package will automatically download a required file from the GitHub repository or a mirror website.
If you need all the project files, to use `imtoolkit` offline, it is recommended to obtain the whole package from GitHub as follows:

    > pip install git+https://github.com/imtoolkit/imtoolkit

The IMToolkit development team welcomes other researchers' contributions and pull requests.
In that case, it would be better to install the latest package and activate the editable mode as follows:

    > git clone https://github.com/imtoolkit/imtoolkit
    > pip install -e ./imtoolkit # this activates the editable mode

<a href="https://ishikawa.cc/imtoolkit/tutorial.html" target="_blank">A detailed tutorial for the installed imtoolkit command is available here.</a>

## Citations

It would be highly appreciated if you cite the following reference when using IMToolkit.

- [1] N. Ishikawa, ``<a href="https://doi.org/10.1109%2Faccess.2019.2928033" target="_blank">IMToolkit: An open-source index modulation toolkit for reproducible research based on massively parallel algorithms</a>,'' IEEE Access, in press.

Of course, if your project relies on CuPy, the following reference is strongly recommended.

- [2] R. Okuta, Y. Unno, D. Nishino, S. Hido, and C. Loomis, ``<a href="http://learningsys.org/nips17/assets/papers/paper_16.pdf" target="_blank">CuPy: A NumPy-compatible library for NVIDIA GPU calculations</a>,'' in Conference on Neural Information Processing Systems Workshop, Long Beach, CA, USA, Dec. 4-9, 2017.

## Contributor(s)

- Dr. Naoki Ishikawa (<a href="https://ishikawa.cc" target="_blank">Web</a> / <a href="https://scholar.google.co.jp/citations?user=JHnisGYAAAAJ" target="_blank">Google Scholar</a> / <a href="https://www.researchgate.net/profile/Naoki_Ishikawa" target="_blank">ResearchGate</a> / <a href="https://publons.com/researcher/3012020/naoki-ishikawa/" target="_blank">Publons</a>)
- You might become a valuable contributor of this project. Any contributions and issues are appreciated.


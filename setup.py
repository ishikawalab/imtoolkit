# (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt.

from setuptools import setup, find_packages
from codecs import open
from os import path
from imtoolkit.__init__ import IMTOOLKIT_VERSION

setup(name='imtoolkit',
      version=IMTOOLKIT_VERSION,
      description='IMToolkit: An open-source index modulation toolkit for reproducible research based on massively parallel algorithms',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      url='https://ishikawa.cc/imtoolkit/',
      download_url="https://pypi.org/project/imtoolkit/",
      author='Naoki Ishikawa',
      author_email='contact@ishikawa.cc',
      license='MIT',
      packages=['imtoolkit'],
      install_requires=[
          'numpy', 'pandas', 'scipy', 'sympy', 'numba', 'tqdm' # cupy
      ],
      entry_points={
          'console_scripts': [
              'imtoolkit = imtoolkit.imtoolkit:main',
              'imsearch = imtoolkit.imsearch:main',
          ]
      },
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7'
      ],
      test_suite='imtoolkit.tests',
      zip_safe=False,
      package_data={'imtoolkit': ['inds/M=2_K=1_Q=2_minh=2_ineq=0.txt', 'inds/M=4_K=1_Q=4_minh=2_ineq=0.txt', 'M=4_K=2_Q=4_minh=2_ineq=0.txt', 'M=4_K=3_Q=4_minh=2_ineq=0.txt']},
)


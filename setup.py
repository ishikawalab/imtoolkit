# (c) IMToolkit Development Team
# This toolkit is released under the MIT License, see LICENSE.txt.

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='imtoolkit',
      version='0.2',
      description='',
      long_description=long_description,
      url='https://ishikawa.cc/imtoolkit/',
      download_url="https://pypi.org/project/imtoolkit/",
      author='Naoki Ishikawa',
      author_email='contact@ishikawa.cc',
      license='MIT',
      packages=['imtoolkit'],
      install_requires=[
          'numba', 'numpy', 'pandas', 'scipy', 'sympy', 'tqdm' # cupy
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
      package_data={'imtoolkit': ['decs/*.txt']},
)


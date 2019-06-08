#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
.. py:currentmodule:: setup.py

Setup for this package
"""
import io
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'py_prod_bootstrap'
DESCRIPTION = 'Python production code bootstrap'
URL = 'https://github.com/fgka/python-bootstrap'
EMAIL = ''
AUTHOR = 'Gustavo Kuhn Andriotti'
# https://devguide.python.org/#branchstatus
REQUIRES_PYTHON = '>=3.7.0'  # End-of-life: 2023-06-27
VERSION = 0.1
CLASSIFIERS = [
    # Trove classifiers
    # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    'License :: OSI Approved :: The MIT License (MIT)'
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Operating System :: OS Independent',
]

# What packages are required for this module to be executed?
INSTALL_REQUIRED = ['deepdiff>=4.0.6']

DEBUG_REQUIRED = ['ipython>=7.5.0']

CODE_QUALITY_REQUIRED = [
    'black==18.9b0',  # bug with vim plugin in version 19.3b0
    'mock>=3.0.5',
    'nose>=1.3.7',
    'pudb>=2019.1',
    'pylama>=7.7.1',
    'pylama-pylint>=3.1.1',
    'pylint>=2.3.1',
    'pytest>=4.5.0',
    'pytest-cov>=2.7.1',
    'pytest-mock>=1.10.4',
    'pytest-pudb>=0.7.0',
    'pytest-pylint>=0.14.0',
    'pytest-xdist>=1.28.0',
    'vulture>=1.0',
]

# What packages are required for this module's docs to be built
DOCS_REQUIRED = ['Sphinx>=2.0.1']

EXTRA_REQUIRED = {'docs': DOCS_REQUIRED, 'tests': CODE_QUALITY_REQUIRED}
EXTRA_REQUIRED['dev'] = (
    EXTRA_REQUIRED['docs'] + EXTRA_REQUIRED['tests'] + DEBUG_REQUIRED
)

HERE = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
        LONG_DESCRIPTION = '\n' + f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
ABOUT = {}
if not VERSION:
    with open(os.path.join(HERE, NAME, '__version__.py')) as f:
        # pylint: disable=exec-used
        exec(f.read(), ABOUT)
else:
    ABOUT['__version__'] = VERSION


# Where the magic happens:
setup(
    name=NAME,
    version=ABOUT['__version__'],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    install_requires=INSTALL_REQUIRED,
    extras_require=EXTRA_REQUIRED,
    include_package_data=True,
    license='MIT',
    packages=find_packages(exclude=('tests',)),
    classifiers=CLASSIFIERS,
)

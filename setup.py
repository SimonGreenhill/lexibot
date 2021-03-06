#!/usr/bin/env python3
# coding=utf-8
# pragma: no cover
import io
import os
import sys

from setuptools import setup, find_packages

# Package meta-data.
NAME = 'lexibot'
DESCRIPTION = ''
URL = ''
EMAIL = ''
AUTHOR = '),'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1'


here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    url=URL,
    packages=find_packages(),
    install_requires=['pylexibank', 'virtualenv', 'GitPython'],
    include_package_data=True,
    entry_points={
        'console_scripts': ['lexibot=lexibot.__main__:main'],
    },
    license='BSD',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
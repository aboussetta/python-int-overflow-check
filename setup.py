#!/usr/bin/env python

import sys
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

install_requires = ['MySQL-python>=1.2']
if sys.version_info < (2, 7):
    install_requires.append('argparse>=1.2')

f = open('int_overflow_check/version.py')
if f:
    exec(f.read())
    f.close()

setup(
    name='int-overflow-check',
    version=__version__,
    author='PalominoDB',
    author_email='oss@palominodb.com',
    packages=find_packages(exclude=['tests']),
    url="http://pypi.python.org/pypi/int-overflow-check",
    license='GPLv2',
    description='Check MySQL tables for potential integer overflows',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'pdb_check_maxvalue = int_overflow_check.pdb_check_maxvalue:main',
        ]
    }
)

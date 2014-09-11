#!/usr/bin/env python
import os
from setuptools import setup


# Get whatever in README.md and assign it to the `long_description` var.
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()


setup(
    name='pathresolver',
    version='0.1',
    description='Resolve nested object paths',
    author='Andrew Crosio',
    long_description=long_description,
    packages=['pathresolver'],
    include_package_data=True,
    test_module=['tests'],
    setup_requires=[],
    install_requires=[],
    test_suite='tests',
    tests_require=[]
)

#!/usr/bin/env python
import os
from setuptools import setup


# Get whatever in README.md and assign it to the `long_description` var.
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()


setup(
    name='pathresolver',
    version='0.1.1',
    description='''
        Path Resolver
        =============

        Resolve paths within nested objects.

        # What is Path Resolver?

        Path Resolver is a very simple piece of python code that allows you to dynamic resolve deeply-nested (or as shallow as you please)
        structures in Python.

        # Why would I use this?

        Path Resolver was born out of a need to dynamically find data within nested JSON information.

        For example, perhaps I want to extract a bunch of information from a dictionary deep within a JSON structure.
        I could, for example, simple write a lot of code and hard-coded indexes, key lookups, et cetera.

        Or, alternatively, I could use a simple DSL to look up and resolve the items I need. This is what Path Resolver is.

        # Example Usage

        ## Simple Usage

        >>> resolve(['testvalue'], 0)
        ['testvalue']

        >>> resolve(['testvalue'], '0')
        'testvalue'

        >>> resolve(['testvalue'], '*')
        ['testvalue']

        >>> resolve({'key': 'testvalue'}, 'key')
        'testvalue'

        >>> resolve({'key': 'testvalue'}, '*')
        ['testvalue']

        ## Advanced Usage

        >>> resolve({'parent': ['one', 'two', 'three']}, 'parent.*')
        ['one', 'two', 'three']

        >>> resolve({'parent': [{'child': 'testvalue1'}]}, 'parent.*.child')
        ['testvalue1']

        >>> resolve({'parent': [{'child': 'testvalue1'}, {'child': 'testvalue2'}]}, 'parent.*.child')
        ['testvalue1', 'testvalue2']

        >>> resolve({'parent': {'child1': 'testvalue1', 'child2': 'testvalue2'}}, 'parent.*')
        ['testvalue1', 'testvalue2']
    ''',
    author='Andrew Crosio',
    author_email='andrew@andrewcrosio.com',
    url='https://github.com/Andrew-Crosio/pathresolver',
    long_description=long_description,
    packages=['pathresolver'],
    include_package_data=True,
    test_module=['tests'],
    setup_requires=[],
    install_requires=[],
    test_suite='tests',
    tests_require=[]
)

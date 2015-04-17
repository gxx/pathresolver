#!/usr/bin/env python
from setuptools import setup
from setuptools import find_packages


setup(
    name='pathresolver',
    version='0.2.1',
    description='Resolve paths within nested objects.',
    long_description='''
        Path Resolver
        =============

        Resolve paths within nested objects.


        Build Status:     https://travis-ci.org/gxx/pathresolver

        Coverage:         https://coveralls.io/r/Andrew-Crosio/pathresolver


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


        ## Functions

        If items along your path are any type of bound, unbound or named functions, they will not be resolved unless
        either forced (see next section), or normal evaluation fails.

        Evaluation of functions works along a back-tracking methodology, ensuring that if it is possible to resolve the
        path specified without resolving any functions, then it will be resolved without any calls.

        >>> function test_func():
        ...    return {'a': 1}
        ... test_func.a = 0

        >>> resolve(Test, 'a')
        0

        If you wish you specifically resolve function calls, you can use manual function resolution as described in the
        next section.


        ### Manually resolving functions

        It's possible to manually resolve or force the resolution of a function call while resolving.

        There are two possible reasons for considering using this:

        1.  Your last attribute is a function you'd wish to resolve.

            Given a path such as ```"a.b"```, if b is a function, it will not be resolved during evaluation due to lazy
            function resolving. If you'd wish to get the result of the function call, rather then the function itself you can

            >>> function test_func():
            ...    return {'a': 1}
            ... test_func.a = 0

            >>> resolve(Test, 'a')
            0

        2.  You wish to either explicitly specify these resolution for explictness' sake or to optimize for wasted cycles.

            Explictness is key (though a little magic doesn't go astray). And you can use the manual function calls for this,
            if you wish.

            Another benefit is that there are no wasted cycles attempting to resolve the value of the function rather than its
            result.

            >>> class Nested(object):
            ...      def me(self):
            ...          return self
            ...      def value(self):
            ...          return 1


            >>> resolve(Nested(), 'me().me().value()')
            1


        ## Working with Objects

        PathResolver will work with objects just as easily as primitives.

        >>> class Test:
        ...    class Nested:
        ...        attribute = 1

        >>> resolve(locals(), 'Test.Nested.attribute')
        1



    ''',
    author='Andrew Crosio',
    author_email='andrew@andrewcrosio.com',
    url='https://github.com/Andrew-Crosio/pathresolver',
    packages=find_packages(),
    include_package_data=True,
    setup_requires=[],
    install_requires=[],
    test_suite='tests',
    tests_require=[]
)

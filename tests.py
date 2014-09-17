#!/usr/bin/env python
# encoding=utf-8
"""pathresolver.py test cases"""
from unittest import TestCase

from pathresolver import resolve
from pathresolver import BadValueError
from pathresolver import NoMatchError


class IterativeObject(object):
    def __init__(self, items):
        self.items = items

    def __iter__(self):
        return iter(self.items)


class GetItemObject(object):
    def __init__(self, items):
        self.items = items

    def __getitem__(self, key):
        return self.items[key]


EQUALITY_TEST_SETS = [
    (['testvalue'], '0', 'testvalue'),
    (['testvalue'], '*', ['testvalue']),
    ({'key': 'testvalue'}, 'key', 'testvalue'),
    ({'key': 'testvalue'}, '*', ['testvalue']),
    ({0: 'testvalue'}, '0', 'testvalue'),
    ({'parent': ['one', 'two', 'three']}, 'parent.*', ['one', 'two', 'three']),
    ({'parent': [{'child': 'testvalue1'}]}, 'parent.*.child', ['testvalue1']),
    ({'parent': [{'child': {'testvalue1'}}]}, 'parent.*.child', [{'testvalue1'}]),
    ({'parent': [{'child': 'testvalue1'}, {'child': 'testvalue2'}]}, 'parent.*.child', ['testvalue1', 'testvalue2']),
    ({'parent': {'child1': 'testvalue1', 'child2': 'testvalue2'}}, 'parent.*', ['testvalue1', 'testvalue2']),
    ({'parent': IterativeObject([{'child': 'testvalue1'}, {'child': 'testvalue2'}])}, 'parent.*.child', ['testvalue1', 'testvalue2']),
    ({'parent': GetItemObject([{'child': 'testvalue1'}, {'child': 'testvalue2'}])}, 'parent.*.child', ['testvalue1', 'testvalue2']),
    ({'some': ['other', 'structure']}, 'something.else.entirely.*', None),
    ({'some': [{'nested': [1, 2]}, {'nested': [3, 4]}]}, 'some.*.nested.*', [[1, 2], [3, 4]]),
]

EXCEPTION_TEST_SETS = [
    (object(), '*', BadValueError),
    ({'some': ['other', 'structure']}, 'something.else.entirely.*', NoMatchError),
    ({'some': None}, 'some.*', BadValueError),
    ({'some': [{'empty': 'sets'}]}, 'some.*.other', NoMatchError)
]


class EqualityTestGenerator(object):
    @staticmethod
    def _generate_test(data, path, expected):
        return lambda self: self.assertEqual(resolve(data, path, default=None), expected)

    def __new__(cls, *args, **kwargs):
        test_funcs = {}

        for num, (test_data, test_path, test_result) in enumerate(EQUALITY_TEST_SETS):
            test_name = 'test_equality_{num}'.format(num=num + 1)
            test_funcs[test_name] = cls._generate_test(test_data, test_path, test_result)

        test_klass = type('PathResolverEqualityTests', (TestCase,), test_funcs)

        return test_klass


class ExceptionTestGenerator(object):
    @staticmethod
    def _generate_test(data, path, expected):
        return lambda self: self.assertRaises(expected, lambda: resolve(data, path))

    def __new__(cls, *args, **kwargs):
        test_funcs = {}

        for num, (test_data, test_path, test_result) in enumerate(EXCEPTION_TEST_SETS):
            test_name = 'test_exception_{num}'.format(num=num + 1)
            test_funcs[test_name] = cls._generate_test(test_data, test_path, test_result)

        test_klass = type('PathResolverExceptionTests', (TestCase,), test_funcs)

        return test_klass


PathResolverEqualityTests = EqualityTestGenerator()

PathResolverExceptionTests = ExceptionTestGenerator()


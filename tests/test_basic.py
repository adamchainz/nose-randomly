# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import os
import sys
from itertools import islice
from unittest import TestCase

from nose.plugins import PluginTester
from nose_randomly import RandomlyPlugin

fixtures = os.path.join(os.path.dirname(__file__), 'fixtures')


class RandomlyPluginTester(PluginTester):
    activate = '--with-randomly'

    def __init__(self, *args, **kwargs):
        super(RandomlyPluginTester, self).__init__(*args, **kwargs)
        self.maxDiff = 10000

    @property
    def plugins(self):
        return [RandomlyPlugin()]

    @property
    def suitepath(self):
        return os.path.join(fixtures, self.fixture_suite)

    def check_output_like(self, lines):
        output = [line.strip() for line in islice(self.output, len(lines))]
        self.assertEqual(output, lines)


class ShuffledSubmmodulesInPackageTest(RandomlyPluginTester, TestCase):
    """
    Check that the submodules inside a package are shuffled.
    """
    args = ['-v']
    if sys.version_info >= (3, 0):  # Python 3 random changes
        args.append('--randomly-seed=15')
    else:
        args.append('--randomly-seed=41')

    fixture_suite = 'abcd_package'

    def runTest(self):
        self.check_output_like([
            'Using ' + self.args[-1],
            'test_it (abcd_package.test_d.D) ... ok',
            'test_it (abcd_package.test_c.C) ... ok',
            'test_it (abcd_package.test_a.A) ... ok',
            'test_it (abcd_package.test_b.B) ... ok'
        ])


class ShuffledCasesInModuleTest(RandomlyPluginTester, TestCase):
    """
    Check that the cases inside a module are shuffled.
    """
    args = ['-v']
    if sys.version_info >= (3, 0):  # Python 3 random changes
        args.append('--randomly-seed=38')
    else:
        args.append('--randomly-seed=56')

    fixture_suite = 'abcd_cases.py'

    def runTest(self):
        self.check_output_like([
            'Using ' + self.args[-1],
            'test_it (abcd_cases.C) ... ok',
            'test_it (abcd_cases.A) ... ok',
            'test_it (abcd_cases.B) ... ok',
            'test_it (abcd_cases.D) ... ok'
        ])


class DontShuffledCasesInModuleTest(RandomlyPluginTester, TestCase):
    """
    Check that the cases inside a module are not shuffled when the 'dont' flag
    is set.
    """
    args = ['-v', '--randomly-seed=1', '--randomly-dont-shuffle-modules']
    fixture_suite = 'abcd_cases.py'

    def runTest(self):
        self.check_output_like([
            'Using --randomly-seed=1',
            'test_it (abcd_cases.A) ... ok',
            'test_it (abcd_cases.B) ... ok',
            'test_it (abcd_cases.C) ... ok',
            'test_it (abcd_cases.D) ... ok'
        ])


class ShuffledTestsInTestCaseTest(RandomlyPluginTester, TestCase):
    """
    Check that the tests inside a case are shuffled.
    """
    args = ['-v']
    if sys.version_info >= (3, 0):  # Python 3 random changes
        args.append('--randomly-seed=126')
    else:
        args.append('--randomly-seed=1')

    fixture_suite = 'abcd_tests.py'

    def runTest(self):
        self.check_output_like([
            'Using ' + self.args[-1],
            'test_D (abcd_tests.Tests) ... ok',
            'test_B (abcd_tests.Tests) ... ok',
            'test_C (abcd_tests.Tests) ... ok',
            'test_A (abcd_tests.Tests) ... ok'
        ])


class DontShuffledTestsInTestCaseTest(RandomlyPluginTester, TestCase):
    """
    Check that the tests inside a case are not shuffled when the 'dont' flag is
    set.
    """
    args = ['-v', '--randomly-seed=1', '--randomly-dont-shuffle-cases']
    fixture_suite = 'abcd_tests.py'

    def runTest(self):
        self.check_output_like([
            'Using --randomly-seed=1',
            'test_A (abcd_tests.Tests) ... ok',
            'test_B (abcd_tests.Tests) ... ok',
            'test_C (abcd_tests.Tests) ... ok',
            'test_D (abcd_tests.Tests) ... ok'
        ])


class NotAlwaysOnTests(RandomlyPluginTester, TestCase):
    """
    Check that if we don't activate the plugin using --with-randomly, then it
    doesn't do any shuffling or output.
    """
    activate = '-v'  # Abuse of this to fill in args - it can't be None :(
    fixture_suite = 'abcd_tests.py'

    def runTest(self):
        self.check_output_like([
            'test_A (abcd_tests.Tests) ... ok',
            'test_B (abcd_tests.Tests) ... ok',
            'test_C (abcd_tests.Tests) ... ok',
            'test_D (abcd_tests.Tests) ... ok'
        ])

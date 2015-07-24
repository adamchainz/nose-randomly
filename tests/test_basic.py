# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import os
import sys
from unittest import TestCase

from nose.plugins import PluginTester
from nose_randomly import RandomlyPlugin

fixtures = os.path.join(os.path.dirname(__file__), 'fixtures')


class RandomlyPluginTester(PluginTester):
    activate = '--with-randomly'

    @property
    def plugins(self):
        return [RandomlyPlugin()]

    @property
    def suitepath(self):
        return os.path.join(fixtures, self.fixture_suite)


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
        self.assertEqual(
            [line.strip() for line in self.output][:5],
            ['Using ' + self.args[-1],
             'test_it (abcd_cases.C) ... ok',
             'test_it (abcd_cases.A) ... ok',
             'test_it (abcd_cases.B) ... ok',
             'test_it (abcd_cases.D) ... ok']
        )


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
        self.assertEqual(
            [line.strip() for line in self.output][:5],
            ['Using ' + self.args[-1],
             'test_D (abcd_tests.Tests) ... ok',
             'test_B (abcd_tests.Tests) ... ok',
             'test_C (abcd_tests.Tests) ... ok',
             'test_A (abcd_tests.Tests) ... ok']
        )


class NotAlwaysOnTests(RandomlyPluginTester, TestCase):
    """
    Check that if we don't activate the plugin using --with-randomly, then it
    doesn't do any shuffling or output.
    """
    activate = '-v'  # Abuse of this to fill in args - it can't be None :(
    fixture_suite = 'abcd_tests.py'

    def runTest(self):
        self.assertEqual(
            [line.strip() for line in self.output][:4],
            ['test_A (abcd_tests.Tests) ... ok',
             'test_B (abcd_tests.Tests) ... ok',
             'test_C (abcd_tests.Tests) ... ok',
             'test_D (abcd_tests.Tests) ... ok']
        )

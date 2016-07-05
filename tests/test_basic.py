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
        self.output = list(self.output)
        output = [line.strip() for line in self.output[:len(lines)]]
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


class RandomSeedTest(RandomlyPluginTester, TestCase):
    """
    Check that the random seed is being set.
    """
    args = ['-v', '--randomly-seed=1']
    fixture_suite = 'random_number.py'

    def runTest(self):
        # Just runs the test - the remaining logic is in the file itself,
        # checking that random.random() gives result it should when seed = 1
        self.check_output_like([
            'Using --randomly-seed=1',
            'test_random (random_number.Tests) ... ok'
        ])


class RandomSeedClassTest(RandomlyPluginTester, TestCase):
    """
    Check that the random seed is being set for any code that might run in
    setUpClass too.
    """
    args = ['-v', '--randomly-seed=1']
    fixture_suite = 'random_number_class.py'

    def runTest(self):
        # Just runs the test - the remaining logic is in the file itself,
        # checking that random.random() gives result it should when seed = 1
        self.check_output_like([
            'Using --randomly-seed=1',
            'test_random_again (random_number_class.TestsAgain) ... ok',
            'test_random (random_number_class.Tests) ... ok',
        ])


class DontRandomSeedTest(RandomlyPluginTester, TestCase):
    """
    Check that the random seed is being set.
    """
    args = ['-v', '--randomly-dont-reset-seed']
    fixture_suite = 'random_seed_not_100.py'

    def runTest(self):
        # Just runs the test - the remaining logic is in the file itself,
        # checking that random.random() does not look like the seed is 100
        self.check_output_like([
            'test_not_reseeded_to_100 (random_seed_not_100.Tests) ... ok'
        ])


class GeneratorTest(RandomlyPluginTester, TestCase):
    """
    Check generator support.
    """
    args = ['-v', '--randomly-seed=83']
    fixture_suite = 'abcd_generator.py'

    def runTest(self):
        self.check_output_like([
            "Using --randomly-seed=83",
            "abcd_generator.test_generator('A',) ... ok",
            "abcd_generator.test_generator('B',) ... ok",
            "abcd_generator.test_generator('C',) ... ok",
            "abcd_generator.test_generator('D',) ... ok",
        ])


class SetuptoolsIntegrationTest(TestCase):
    """
    Ensure nose-randomly works when Nose is invoked via setuptools.
    See https://github.com/adamchainz/nose-randomly/issues/11
    """
    def runTest(self):
        import nose.commands

        from setuptools import Command
        from distutils.dist import Distribution
        from nose.config import Config, user_config_files
        from nose.plugins import PluginManager

        class DummyNose(Command):
            description = "Dummy"
            manager = PluginManager()
            manager.plugins = [RandomlyPlugin()]
            __config = Config(
                files=user_config_files(),
                plugins=manager)
            __parser = __config.getParser()
            user_options = nose.commands.get_user_options(__parser)

            def initialize_options(self):
                pass

            def finalize_options(self):
                pass

            def run(self):
                pass

        dist = Distribution({'cmdclass': {'nosetests': DummyNose}})
        dist.script_args = ['nosetests']

        # This test should merely not throw an exception
        dist.parse_command_line()

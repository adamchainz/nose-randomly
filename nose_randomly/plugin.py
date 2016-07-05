# -*- encoding:utf-8 -*-
from __future__ import division, print_function, unicode_literals

import random
import sys
import time

from nose.plugins import Plugin
from nose.suite import ContextList

# factory-boy
try:
    from factory.fuzzy import set_random_state as factory_set_random_state
    have_factory_boy = True
except ImportError:
    have_factory_boy = False

# fake-factory
try:
    from faker.generator import random as faker_random
    have_faker = True
except ImportError:
    have_faker = False

# Compat
if sys.version_info[0] == 2:  # Python 2
    map_return_type = list
else:
    map_return_type = map


class RandomlyPlugin(Plugin):
    name = str('randomly')

    def options(self, parser, env):
        """Register commandline options.
        """
        super(RandomlyPlugin, self).options(parser, env)
        parser.add_option(
            str('--randomly-seed'), action='store', dest='seed',
            default=int(time.time()), type=int,
            help="""Set the seed that nose-randomly uses. Default behaviour:
                    use time.time()"""
        )
        parser.add_option(
            str('--randomly-dont-shuffle-modules'), action='store_false',
            dest='shuffle_modules', default=True,
            help="Stop nose-randomly from shuffling the tests inside modules"
        )
        parser.add_option(
            str('--randomly-dont-shuffle-cases'), action='store_false',
            dest='shuffle_cases', default=True,
            help="""Stop nose-randomly from shuffling the tests inside TestCase
                    classes"""
        )
        parser.add_option(
            str('--randomly-dont-reset-seed'), action='store_false',
            dest='reset_seed', default=True,
            help="""Stop nose-randomly from resetting random.seed() at the
                    start of every test context (TestCase) and test."""
        )

    def configure(self, options, conf):
        """
        Configure plugin.
        """
        super(RandomlyPlugin, self).configure(options, conf)

        if not self.enabled:
            return

        self.options = options

    def setOutputStream(self, stream):
        if not self.enabled:
            return

        self.output_stream = stream

        if self.options.reset_seed:
            print(
                "Using --randomly-seed={seed}".format(seed=self.options.seed),
                file=self.output_stream
            )

    def startContext(self, context):
        self.reset_random_seed()

    def startTest(self, test):
        self.reset_random_seed()

    def reset_random_seed(self):
        if not self.enabled:
            return

        if self.options.reset_seed:
            random.setstate(self.random_state)

            if have_factory_boy:
                factory_set_random_state(self.random_state)

            if have_faker:
                faker_random.setstate(self.random_state)

    @property
    def random_state(self):
        if not hasattr(self, '_random_state'):
            random.seed(self.options.seed)
            self._random_state = random.getstate()
        return self._random_state

    def prepareTestLoader(self, loader):
        """
        Randomize the order of tests loaded from modules and from classes.

        This is a hack. We take the class of the existing, passed in loader
        (normally nose.loader.Loader) and subclass it to monkey-patch in
        shuffle calls for module and case loading when they requested, and then
        mutate the existing test loader's class to this new subclass.

        This is somewhat horrible, but nose's plugin infrastructure isn't so
        flexible - there is no way to wrap just the loader without risking
        interfering with other plugins (if you return anything, no other plugin
        may do anything to the loader).
        """
        if not self.enabled:
            return

        options = self.options

        class ShuffledLoader(loader.__class__):
            def loadTestsFromModule(self, *args, **kwargs):
                """
                Temporarily wrap self.suiteClass with a function that shuffles
                any ContextList instances that the super() call will pass it.
                """
                if options.shuffle_modules:
                    orig_suiteClass = self.suiteClass

                    def hackSuiteClass(tests, **kwargs):
                        if isinstance(tests, ContextList):
                            random.seed(options.seed)
                            random.shuffle(tests.tests)
                        return orig_suiteClass(tests, **kwargs)

                    self.suiteClass = hackSuiteClass
                suite = super(ShuffledLoader, self).loadTestsFromModule(
                    *args, **kwargs)

                if options.shuffle_modules:
                    self.suiteClass = orig_suiteClass

                return suite

            def loadTestsFromTestCase(self, testCaseClass):
                """
                Temporarily wrap self.suiteClass with a function that shuffles
                any list of tests that the super() call will pass it.
                """
                if options.shuffle_cases:
                    orig_suiteClass = self.suiteClass

                    def hackSuiteClass(tests, **kwargs):
                        if isinstance(tests, map_return_type):
                            tests = list(tests)
                            random.seed(options.seed)
                            random.shuffle(tests)
                        return orig_suiteClass(tests, **kwargs)

                    self.suiteClass = hackSuiteClass

                suite = super(ShuffledLoader, self).loadTestsFromTestCase(
                    testCaseClass)

                if options.shuffle_cases:
                    self.suiteClass = orig_suiteClass

                return suite

        # Directly mutate the class of loader... eww
        loader.__class__ = ShuffledLoader

        # Tell the plugin infrastructure we did nothing so 'loader', as mutated
        # above, continues to be used
        return None

# -*- encoding:utf-8 -*-
from __future__ import division, print_function, unicode_literals

import random
import time

from nose.plugins import Plugin
from nose.suite import ContextList

try:
    from factory.fuzzy import set_random_state as factory_set_random_state
    have_factory_boy = True
except ImportError:
    have_factory_boy = False


class RandomlyPlugin(Plugin):
    name = 'randomly'

    def options(self, parser, env):
        """Register commandline options.
        """
        super(RandomlyPlugin, self).options(parser, env)
        parser.add_option(
            '--randomly-seed', action='store', dest='random_seed',
            default=None, type=int,
            help="""Set the seed that nose-randomly uses. Default behaviour:
                    use time.time()"""
        )

    def configure(self, options, conf):
        """
        Configure plugin.
        """
        super(RandomlyPlugin, self).configure(options, conf)

        self.random_seed = options.random_seed
        if self.random_seed is None:
            self.random_seed = int(time.time())

    def setOutputStream(self, stream):
        self.output_stream = stream
        print(
            "Using --randomly-seed={seed}".format(seed=self.random_seed),
            file=self.output_stream
        )

    def startTest(self, test):
        random.seed(self.random_seed)

        if have_factory_boy:
            factory_set_random_state(random.getstate())

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
        the_seed = self.random_seed

        class ShuffledLoader(loader.__class__):
            def loadTestsFromModule(self, *args, **kwargs):
                """
                Temporarily wrap self.suiteClass with a function that shuffles
                any ContextList instances that the super() call will pass it.
                """
                orig_suiteClass = self.suiteClass

                def hackSuiteClass(tests):
                    if isinstance(tests, ContextList):
                        random.seed(the_seed)
                        random.shuffle(tests.tests)
                    return orig_suiteClass(tests)

                self.suiteClass = hackSuiteClass
                suite = super(ShuffledLoader, self).loadTestsFromModule(
                    *args, **kwargs)
                self.suiteClass = orig_suiteClass

                return suite

            def loadTestsFromTestCase(self, testCaseClass):
                """
                Temporarily wrap self.suiteClass with a function that shuffles
                any list of tests that the super() call will pass it.
                """
                orig_suiteClass = self.suiteClass

                def hackSuiteClass(tests):
                    if isinstance(tests, (list, map)):  # map is a type on PY3
                        tests = list(tests)
                        random.seed(the_seed)
                        random.shuffle(tests)
                    return orig_suiteClass(tests)

                self.suiteClass = hackSuiteClass
                suite = super(ShuffledLoader, self).loadTestsFromTestCase(
                    testCaseClass)
                self.suiteClass = orig_suiteClass

                return suite

        # Directly mutate the class of loader... eww
        loader.__class__ = ShuffledLoader

        # Tell the plugin infrastructure we did nothing so 'loader', as mutated
        # above, continues to be used
        return None

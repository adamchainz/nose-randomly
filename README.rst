=============
nose-randomly
=============

.. image:: https://img.shields.io/travis/adamchainz/nose-randomly.svg
        :target: https://travis-ci.org/adamchainz/nose-randomly

.. image:: https://img.shields.io/pypi/v/nose-randomly.svg
        :target: https://pypi.python.org/pypi/nose-randomly

.. figure:: https://raw.githubusercontent.com/adamchainz/nose-randomly/master/logo.png
   :scale: 50%
   :alt: Randomness power.

Nose plugin to randomly order tests and control ``random.seed``. (Also
available `for pytest <https://github.com/adamchainz/pytest-randomly>`_).

Features
--------

All of these features are on by default but can be disabled with flags.

* Randomly shuffles the submodules, ``TestCase`` classes + test functions when
  loading a module of tests.
* Randomly shuffles the test functions inside a ``TestCase`` when loading it.
* Resets ``random.seed()`` at the start of every test case and test to a fixed
  number - this defaults to ``time.time()`` from the start of your test run,
  but you can pass in ``--randomly-seed`` to repeat a randomness-induced
  failure.
* If
  `factory boy <https://factoryboy.readthedocs.io/en/latest/reference.html>`_
  is installed, its random state is reset at the start of every test. This
  allows for repeatable use of its random 'fuzzy' features.
* If `faker <https://pypi.python.org/pypi/fake-factory>`_ is installed, its
  random state is reset at the start of every test. This is also for repeatable
  fuzzy data in tests - factory boy uses faker for lots of data.

About
-----

Randomness in testing can be quite powerful to discover hidden flaws in the
tests themselves, as well as giving a little more coverage to your system.

By randomly ordering the tests, the risk of surprising inter-test dependencies
is reduced - a technique used in many places, for example Google's C++ test
runner `googletest
<https://code.google.com/p/googletest/wiki/V1_5_AdvancedGuide#Shuffling_the_Tests>`_.

By resetting the random seed to a repeatable number for each test, tests can
create data based on random numbers and yet remain repeatable, for example
factory boy's fuzzy values. This is good for ensuring that tests specify the
data they need and that the tested system is not affected by any data that is
filled in randomly due to not being specified.

Requirements
------------

Tested with:

* Python 2.7, 3.4, 3.5
* The latest version of Nose

Usage
-----

Install from pip with:

.. code-block:: bash

    pip install nose-randomly

Nose will automatically find the plugin.

To activate it on your test run, use the ``--with-randomly`` flag, for example:

.. code-block:: bash

    nosetests -v --with-randomly

The output will start with an extra line that tells you the random seed that is
being used:

.. code-block:: bash

    Using --randomly-seed=1234
    test_D (abcd_tests.Tests) ... ok
    ...

If the tests then fail due to ordering or randomly created data, you can then
restart them with that seed:

.. code-block:: bash

    nosetests -v --with-randomly --randomly-seed=1234

You can disable behaviours you don't like with the following flags:

* ``--randomly-dont-shuffle-modules`` - turn off the shuffling of the contents
  of modules
* ``--randomly-dont-shuffle-cases`` - turn off the shuffling of test functions
  inside ``TestCase`` classes
* ``--randomly-dont-reset-seed`` - turn off the reset of ``random.seed()`` at
  the start of every test


Background
----------

`nose` has an `unmerged pull request
<https://code.google.com/p/python-nose/issues/detail?id=255>`_ from 2009 to add
random ordering functionality. This is available in plugin format in the
`nose-randomize <https://github.com/nloadholtes/nose-randomize/>`_ package. It
works quite well but I found that since it replaces all of the test loading
machinery inside `nose`, it can interact badly with other plugins. This plugin
was developed as a thinner layer to achieve the same thing, plus the random
seed resetting which was not available before.


License
-------

* BSD licensed, see LICENSE file
* Logo by Christian Mohr from the Noun Project
  (`link <https://thenounproject.com/search/?q=dice&i=110905>`_).

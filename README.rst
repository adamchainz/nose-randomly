=============
nose-randomly
=============

.. image:: https://img.shields.io/travis/adamchainz/nose-randomly.svg
        :target: https://travis-ci.org/adamchainz/nose-randomly

.. image:: https://img.shields.io/pypi/v/nose-randomly.svg
        :target: https://pypi.python.org/pypi/nose-randomly


Nose plugin to randomly order tests and control ``random.seed``.

Features
--------

All of these features default on but can be disabled with commandline flags.

* Randomly shuffles the submodules, ``TestCase`` classes + test functions when
  loading a module of tests.
* Randomly shuffles the test functions inside a ``TestCase`` when loading it.
* Resets ``random.seed()`` at the start of every test to a fixed number -
  this defaults to ``time.time()`` from the start of your test run, but you can
  pass in ``--random-seed`` to repeat a randomness-induced failure.
* If
  `factory boy <https://factoryboy.readthedocs.org/en/latest/reference.html>`_
  is installed, its random state is reset at the start of every test. This
  allows for repeatable use of its random 'fuzzy' features.


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

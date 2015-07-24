=============
nose-randomly
=============

.. image:: https://img.shields.io/travis/adamchainz/nose-randomly.svg
        :target: https://travis-ci.org/adamchainz/nose-randomly

.. image:: https://img.shields.io/pypi/v/nose-randomly.svg
        :target: https://pypi.python.org/pypi/nose-randomly


Nose plugin to randomly order tests and control ``random.seed``.

It will:

* Randomly shuffle the ``TestCase`` classes + test functions when loading a
  module of tests.
* Randomly shuffle the test functions inside a ``TestCase`` when loading it.
* Reset ``random.seed()`` at the start of every test to a fixed number -
  this defaults to ``time.time()`` from the start of your test run, but you can
  pass in ``--random-seed`` to repeat a randomness-induced failure.
* If
  `factory boy <https://factoryboy.readthedocs.org/en/latest/reference.html>`_
  is installed, reset its random state at the start of every test. This allows
  for repeatable use of its random 'fuzzy' features.

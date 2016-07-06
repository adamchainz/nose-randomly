.. :changelog:

History
-------

Pending release
---------------

* New release notes here

1.2.2 (2016-07-06)
------------------

* Fixed to work with ``python setup.py nosetests`` on Python 2 due to issue
  with ``unicode`` not working with ``distutils.fancy_getopt``.

1.2.1 (2016-06-01)
------------------

* Support test generators.

1.2.0 (2015-12-10)
------------------

* Reset the random state for Faker (pip package ``fake-factory``) too

1.1.0 (2015-08-27)
------------------

* Reset the random seed at the start of nose test contexts (TestCases
  etc.) too
* Slight performance improvement by always using ``random.setstate()`` for
  reseeding

1.0.0 (2015-07-23)
------------------

* First release on PyPI.

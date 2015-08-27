.. :changelog:

History
-------

1.1.0 (2015-08-27)
------------------

* Reset the random seed at the start of nose test contexts (TestCases
  etc.) too
* Slight performance improvement by always using ``random.setstate()`` for
  reseeding

1.0.0 (2015-07-23)
------------------

* First release on PyPI.

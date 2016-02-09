
Quickstart
==========

.. image:: https://api.travis-ci.org/alexamici/pytest-wish.svg?branch=master
    :target: https://travis-ci.org/alexamici/pytest-wish/branches
    :alt: Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/alexamici/pytest-wish?branch=master
    :target: https://ci.appveyor.com/project/alexamici/pytest-wish/branch/master
    :alt: Build Status on AppVeyor

.. image:: https://coveralls.io/repos/alexamici/pytest-wish/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/alexamici/pytest-wish?branch=master
    :alt: Coverage Status on Coveralls


With pytest-wish you can search all installed modules for functions
that pass a given feature-specification test suite.

Development status: **almost beta** (but not quite there yet).

Installation
------------
.. code-block:: sh

    $ pip install pytest-wish


Your first "search by tests"
----------------------------

Let's search for a function that robustly parse boolean values from a string.
First, create the ``test_parse_bool.py`` file with a test function asserting
the expected behaviour of the fictional ``parse_bool(text)`` function::

    def test_parse_bool():
        assert not parse_bool('false')
        assert not parse_bool('FALSE')
        assert not parse_bool('0')
        assert parse_bool('true')
        assert parse_bool('TRUE')
        assert parse_bool('1')

Then, instrument the test with the ``wish`` fixture::

    def test_parse_bool(wish):
        parse_bool = wish
        assert not parse_bool('false')
        assert not parse_bool('FALSE')
        assert not parse_bool('0')
        assert parse_bool('true')
        assert parse_bool('TRUE')
        assert parse_bool('1')

Finally, let pytest run the test once for every function in the Python standard library:

.. code-block:: sh

    $ py.test --wish-from-stdlib
    ======================= test session starts ==========================
    platform darwin -- Python 3.5.0, pytest-2.8.7, py-1.4.31, pluggy-0.3.1
    rootdir: /tmp, inifile: setup.cfg
    plugins: wish-0.9.0, timeout-1.0.0
    collected 3259 items

    test_parse_bool.py xxxxxxxxxxxx[...]xxxxxxxxXxxxxxxxx[...]xxxxxxxxxxxx

    ============================== 1 hit =================================

    test_parse_bool.py::test_parse_bool[distutils.util:strtobool] HIT

    ==== 3258 xfailed, 1 xpassed, 27 pytest-warnings in 45.07 seconds ====

The ``strtobool`` function of the ``distutils.util`` module is a HIT, that is it passes the test
and it is in fact a neat implementation of ``parse_bool(text)`` with even more features. Win!


Help
----

We have the following support channels:

* `questions on stackoverflow`_


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.


Contributing
------------

Contributions are very welcome.
Issues and pull requests on the `pytest-wish GitHub repository`_.
Please see the `CONTRIBUTING`_ document for development guidelines.

Authors:

* Alessandro Amici - `@alexamici`_

Contributors:

* `@kr1`_

Sponsors:

.. image:: http://services.bopen.eu/bopen-logo.png
    :target: http://bopen.eu/
    :alt: B-Open Solutions srl


License
-------

Distributed under the terms of the `MIT`_ license, "pytest-wish" is free and open source software


.. _`package documentation`: https://pytest-wish.readthedocs.org
.. _`@kr1`: https://github.com/kr1
.. _`pytest-wish`: https://pytest-wish.readthedocs.org
.. _`the latest version of "pytest-wish"`: https://pypi.python.org/pypi/pytest-wish
.. _`pytest`: https://pytest.org
.. _`questions on stackoverflow`: https://stackoverflow.com/search?q=pytest-wish
.. _`file an issue`: https://github.com/alexamici/pytest-wish/issues
.. _`pytest-wish GitHub repository`: https://github.com/alexamici/pytest-wish
.. _`CONTRIBUTING`: https://github.com/alexamici/pytest-wish/blob/master/CONTRIBUTING.rst
.. _`@alexamici`: https://github.com/alexamici
.. _`MIT`: http://opensource.org/licenses/MIT

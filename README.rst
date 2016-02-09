
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

First timer FAQ
---------------

**Who are pytest-wish users?**

Python developers who've got better things to do than reinvent wheels.

**What is pytest-wish exactly?**

A `pytest <https://pytest.org>`_ plugin
that helps you find functions that pass a given test by searching
in the Python standard library or in all the modules you have installed.

**That sounds interesting, I need a function that robustly parses a boolean value from a string.**
**Here's my specification test**::

    def test_parse_bool():
        assert not parse_bool('false')
        assert not parse_bool('FALSE')
        assert not parse_bool('0')
        assert parse_bool('true')
        assert parse_bool('TRUE')
        assert parse_bool('1')

**How do I search for it?**

First, install the `latest version of pytest-wish <https://pypi.python.org/pypi/pytest-wish>`_
from the Python Package Index::

    $ pip install pytest-wish

Then copy your specification test to the ``test_parse_bool.py`` file and
instrument it with the ``wish`` fixture::

    def test_parse_bool(wish):
        parse_bool = wish
        assert not parse_bool('false')
        assert not parse_bool('FALSE')
        assert not parse_bool('0')
        assert parse_bool('true')
        assert parse_bool('TRUE')
        assert parse_bool('1')

Finally, instruct pytest-wish to run your test on all functions in the Python standard library::

    $ py.test test_parse_bool.py --wish-from-stdlib
    ======================= test session starts ==========================
    platform darwin -- Python 3.5.0, pytest-2.8.7, py-1.4.31, pluggy-0.3.1
    rootdir: /tmp, inifile: setup.cfg
    plugins: wish-0.9.0, timeout-1.0.0
    collected 3259 items

    test_parse_bool.py xxxxxxxxxxxx[...]xxxxxxxxXxxxxxxxx[...]xxxxxxxxxxxx

    ============================== 1 hit =================================

    test_parse_bool.py::test_parse_bool[distutils.util:strtobool] HIT

    ==== 3258 xfailed, 1 xpassed, 27 pytest-warnings in 45.07 seconds ====

And you've got a HIT!
In less than a minute pytest-wish collected more than 3000 functions from the standard library
and run your specification test on all of them.
Only `strtobool`_ in the distutils.util module passes the test, so
now you should thoroughly review it and if you like it you may use it in your code.

.. _`strtobool`: https://docs.python.org/3/distutils/apiref.html#distutils.util.strtobool

**Wow! Does it work so well all the times?**

To be honest strtobool is a little known gem of the Python standard library that
is just perfect for illustrating all the benefits of the "search by tests" strategy.
Here are some of them in rough order of importance:

- a function imported is a one less function coded---and tested, documented, debugged,
  ported, maintained...
- it's battle tested code---lot's of old bugs have already been squashed
- it's other people code---there's an upstream to report new bugs to
- it gives you additional useful functionality---for free on top of that
- it's in the Python standard library---no additional dependency required


Project resources
-----------------

============= ======================
Documentation https://pytest-wish.readthedocs.org
User support  https://stackoverflow.com/search?q=pytest-wish
Development   https://github.com/alexamici/pytest-wish
Discussion    To be decided, see issue `#15 <https://github.com/alexamici/pytest-wish/issues/15>`_
============= ======================

Contributing
------------

Contributions are very welcome. Please see the `CONTRIBUTING`_ document for
the best way to help.
If you encounter any problems, please file an issue along with a detailed description.

.. _`CONTRIBUTING`: https://github.com/alexamici/pytest-wish/blob/master/CONTRIBUTING.rst

Authors:

* Alessandro Amici - `@alexamici <https://github.com/alexamici>`_

Contributors:

* `@kr1 <https://github.com/kr1>`_

Sponsors:

.. image:: http://services.bopen.eu/bopen-logo.png
    :target: http://bopen.eu/
    :alt: B-Open Solutions srl


License
-------

pytest-wish is free and open source software distributed under the terms of the `MIT`_ license.

.. _`MIT`: http://opensource.org/licenses/MIT

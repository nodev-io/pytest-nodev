
.. This document is intended as the main entry point for new users,
   it serves as the landing page on GitHub and on PyPI and
   it is also used as Quickstart section of the docs.
   Its goal are:
   * inspire and raise interest in new users
   * present one complete end-to-end use case
   * warn users of risks and suggest mitigation strategies
   * direct interested users to the appropriate project resource
   * state license and open source nature
   * credit contributors
   Anything else should go into docs.

.. NOTE: only the first line of the README is shown on GitHub mobile

pytest-nodev is a simple test-driven search engine for live code,
it finds classes and functions matching the behaviour specified by the given tests.

Development status: **beta**.

New user FAQ
------------

**What is pytest-nodev?**

To be more precise pytest-nodev is a `pytest <https://pytest.org>`_ plugin
that helps you execute specification tests on all objects
in the Python standard library and in all the modules you have installed.

**Who are pytest-nodev users?**

Python developers who've got better things to do than reinvent wheels.

**Sounds interesting, I need a function that robustly parses a boolean value from a string.**
**Here's my specification test**::

    def test_parse_bool():
        assert not parse_bool('false')
        assert not parse_bool('FALSE')
        assert not parse_bool('0')

        assert parse_bool('true')
        assert parse_bool('TRUE')
        assert parse_bool('1')

**Show me how searching with pytest-nodev work.**

First, install the `latest version of pytest-nodev <https://pypi.python.org/pypi/pytest-nodev>`_
from the Python Package Index::

    $ pip install pytest-nodev

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

Finally, instruct pytest-nodev to run your test on all functions in the Python standard library::

    $ py.test test_parse_bool.py --wish-from-stdlib
    ======================= test session starts ==========================
    platform darwin -- Python 3.5.0, pytest-2.8.7, py-1.4.31, pluggy-0.3.1
    rootdir: /tmp, inifile: setup.cfg
    plugins: nodev-1.0.0, timeout-1.0.0
    collected 3259 items

    test_parse_bool.py xxxxxxxxxxxx[...]xxxxxxxxXxxxxxxxx[...]xxxxxxxxxxxx

    ============================== 1 hit =================================

    test_parse_bool.py::test_parse_bool[distutils.util:strtobool] HIT

    ==== 3258 xfailed, 1 xpassed, 27 pytest-warnings in 45.07 seconds ====

In less than a minute pytest-nodev collected more than 3000 functions from the standard library
and run your specification test on all of them and you've got a HIT.
The `strtobool`_ function in the distutils.util module passes the test, so
now you should thoroughly review it and if you like it you may use it in your code,
no need to write your own implementation.

.. _`strtobool`: https://docs.python.org/3/distutils/apiref.html#distutils.util.strtobool

**Wow! Does it work so well all the times?**

To be honest strtobool is a little known gem of the Python standard library that
is just perfect for illustrating all the benefits of the search-by-tests strategy.
Here are some of them in rough order of importance:

- a function imported is a one less function coded---and tested, documented, debugged,
  ported, maintained...
- it's battle tested code---lot's of old bugs have already been squashed
- it's other people code---there's an upstream to report new bugs to
- it gives you additional useful functionality---for free on top of that
- it's in the Python standard library---no additional dependency required

BIG FAT WARNING!
----------------

A lot of functions called with the wrong set of arguments may have unexpected consequences ranging
from slightly annoying, think ``os.mkdir('false')``,
to **utterly catastrophic**, think ``shutil.rmtree('/', True)``.
Serious use of pytest-nodev, in particular using ``--wish-from-all``,
require operating-system level isolation,
e.g. a dedicated user or even better a dedicated container.

Discussion on how to best help users sandboxing pytest-nodev is ongoing,
see issue `#16 <https://github.com/nodev-io/pytest-nodev/issues/16>`_.


Project resources
-----------------

============= ======================
Documentation http://pytest-nodev.readthedocs.org
Support       https://stackoverflow.com/search?q=pytest-nodev
Development   https://github.com/nodev-io/pytest-nodev
Discussion    To be decided, see issue `#15 <https://github.com/nodev-io/pytest-nodev/issues/15>`_
Download      https://pypi.python.org/pypi/pytest-nodev
Code quality  .. image:: https://api.travis-ci.org/nodev-io/pytest-nodev.svg?branch=master
                :target: https://travis-ci.org/nodev-io/pytest-nodev/branches
                :alt: Build Status on Travis CI
              .. image:: https://ci.appveyor.com/api/projects/status/github/nodev-io/pytest-nodev?branch=master
                :target: https://ci.appveyor.com/project/alexamici/pytest-nodev/branch/master
                :alt: Build Status on AppVeyor
              .. image:: https://coveralls.io/repos/nodev-io/pytest-nodev/badge.svg?branch=master&service=github
                :target: https://coveralls.io/github/nodev-io/pytest-nodev?branch=master
                :alt: Coverage Status on Coveralls
nodev website http://nodev.io
============= ======================


Contributing
------------

Contributions are very welcome. Please see the `CONTRIBUTING`_ document for
the best way to help.
If you encounter any problems, please file an issue along with a detailed description.

.. _`CONTRIBUTING`: https://github.com/nodev-io/pytest-nodev/blob/master/CONTRIBUTING.rst

Authors:

- Alessandro Amici - `@alexamici <https://github.com/alexamici>`_

Contributors:

- `@kr1 <https://github.com/kr1>`_

Sponsors:

- .. image:: http://services.bopen.eu/bopen-logo.png
      :target: http://bopen.eu/
      :alt: B-Open Solutions srl


License
-------

pytest-nodev is free and open source software
distributed under the terms of the `MIT <http://opensource.org/licenses/MIT>`_ license.

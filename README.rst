
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

.. NOTE: only the first couple of lines of the README are shown on GitHub mobile

pytest-nodev is a simple test-driven search engine for Python code,
it finds classes and functions that match the behaviour specified by the given tests.

**How does "test-driven code search" work?**

To be more precise pytest-nodev is a `pytest <https://pytest.org>`_ plugin
that lets you execute a set of tests that specify the expected behaviour of a class or a function
on all objects in the Python standard library and in all the modules you have installed.

**Show me how it works in practice.**
**I need to write a** ``parse_bool`` **function that robustly parses a boolean value from a string.**
**Here is the test I intend to use to validate my own implementation once I write it**:

.. code-block:: python

    def test_parse_bool():
        assert not parse_bool('false')
        assert not parse_bool('FALSE')
        assert not parse_bool('0')

        assert parse_bool('true')
        assert parse_bool('TRUE')
        assert parse_bool('1')

First, install the `latest version of pytest-nodev <https://pypi.python.org/pypi/pytest-nodev>`_
from the Python Package Index:

.. code-block:: console

    $ pip install pytest-nodev

Then copy your specification test to the ``test_parse_bool.py`` file and
decorate it with ``pytest.mark.candidate`` as follows:

.. code-block:: python

    import pytest

    @pytest.mark.candidate('parse_bool')
    def test_parse_bool():
        assert not parse_bool('false')
        assert not parse_bool('FALSE')
        assert not parse_bool('0')

        assert parse_bool('true')
        assert parse_bool('TRUE')
        assert parse_bool('1')

Finally, instruct pytest to run your test on all candidate callables in the Python standard library:

.. code-block:: console

    $ py.test --candidates-from-stdlib test_parse_bool.py
    ======================= test session starts ==========================
    platform darwin -- Python 3.5.1, pytest-2.9.2, py-1.4.31, pluggy-0.3.1
    rootdir: /tmp, inifile: setup.cfg
    plugins: nodev-1.0.0, timeout-1.0.0
    collected 4000 items

    test_parse_bool.py xxxxxxxxxxxx[...]xxxxxxxxXxxxxxxxx[...]xxxxxxxxxxxx

    ====================== pytest_nodev: 1 passed ========================

    test_parse_bool.py::test_parse_bool[distutils.util:strtobool] PASSED

    === 3999 xfailed, 1 xpassed, 260 pytest-warnings in 75.38 seconds ====

In just over a minute pytest-nodev collected 4000 functions from the standard library,
run your specification test on all of them and
reported that the `strtobool`_ function in the distutils.util module
is the only candidate that passes your test.

Now you can review it and if you like it you may use it in your code.
No need to write your own implementation!

.. _`strtobool`: https://docs.python.org/3/distutils/apiref.html#distutils.util.strtobool

**Wow! Does it work so well all the times?**

To be honest strtobool is a little known gem of the Python standard library that
is just perfect for illustrating all the benefits of test-driven code search.
Here are some of them in rough order of importance:

- a function imported is a one less function coded---and tested, documented, debugged,
  ported, maintained...
- it's battle tested code---lot's of old bugs have already been squashed
- it's other people code---there's an upstream to report new bugs to
- it gives you additional useful functionality---for free on top of that
- it's in the Python standard library---no additional dependency required


BIG FAT WARNING!
----------------

Searching code with pytest-nodev looks very much like running arbitrary callables with random arguments.
A lot of functions called with the wrong set of arguments may have unexpected consequences ranging
from slightly annoying, think ``os.mkdir('false')``,
to **utterly catastrophic**, think ``shutil.rmtree('/', True)``.
Serious use of pytest-nodev, in particular using ``--candidates-from-all``,
require running the tests with operating-system level isolation,
e.g. as a dedicated user or even better inside a dedicated container.
The `Starter kit <http://pytest-nodev.readthedocs.io/en/stable/starterkit.html>`_
guide documents how to run pytest-nodev safely and efficiently.


Project resources
-----------------

============= ======================
Documentation http://pytest-nodev.readthedocs.io
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
                :target: https://coveralls.io/github/nodev-io/pytest-nodev
                :alt: Coverage Status on Coveralls
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

- `@calmomau <https://github.com/calmomau>`_
- `@kr1 <https://github.com/kr1>`_

Sponsors:

- .. image:: http://www.bopen.it/wp-content/uploads/2016/01/logo-no-back.png
      :target: http://bopen.eu/
      :alt: B-Open Solutions srl


License
-------

pytest-nodev is free and open source software
distributed under the terms of the `MIT <http://opensource.org/licenses/MIT>`_ license.

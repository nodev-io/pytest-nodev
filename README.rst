pytest-wish
===========

.. image:: https://travis-ci.org/alexamici/pytest-wish.svg?branch=master
    :target: https://travis-ci.org/alexamici/pytest-wish
    :alt: Build Status on Travis CI

.. image:: https://coveralls.io/repos/alexamici/pytest-wish/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/alexamici/pytest-wish
    :alt: Coverage Status on Coveralls

Collects objects from all installed modules and provides them one by one as a fixture.
**Development status: alpha!**


Motivation
----------

    "Have a look at this function that I'm writing...
    I'm sure someone else has already written it." - `@kr1`_

Every piece of functionality in a software project
requires code that lies somewhere in the wide reusability spectrum that goes
form extremely custom and strongly tied to the specific implementation
to completely generic and highly reusable.

On the *custom* side of the spectrum there is all the code that defines the
features of the software and all the choices of its implementation. That one is code that need
to be written.

On the other hand a seasoned software developer is trained to spot
pieces of functionality that lie far enough on the *generic* side of the range
that with high probability a library already implements it
**and documents it well enough to be discovered with an internet search**.

In between the two extremes there is a huge gray area populated by pieces of functionality
that are not *generic* enough to obviously deserve a place in a library, but are
*common* enough that must have been already implemented by someone else for their
software. This kind of code is doomed to be re-implemented again and again
for the simple reason that **there is no way to search code by functionality**...

Or is it?


Test-Driven no-Development
--------------------------

`pytest-wish` is a pytest plugin that enables a software development strategy called
*Test-Driven no-Development* or *nodev* for short, that is an extension of the
*Test-Driven Development* paradigm.

The idea is that once the developer has written the tests that define the behaviour of a new
function to a degree sufficient to validate the implementation they are going to write
it is good enough to validate
any implementation. Running the tests on a large set of functions may result in a *hit*, that is
a function that already implements their feature.

Due to its nature the *nodev* approach is better suited for discovering smaller functions
with a generic signature.


Test suite validation
---------------------

Another use for `pytest-wish` is, with a bit of additional work, to validate a project test suite.
If a test passes when passed an unexpected object there are two possibilities,
either the test is not strict enough and allows for false positives and needs update,
or the *hit* is actually a function you could use instead of your implementation.


Features
--------

* Runs a set of tests over all objects contained in a list of modules.


Requirements
------------

* TODO


Installation
------------

You can install "pytest-wish" via `pip`_ from `PyPI`_::

    $ pip install pytest-wish


Usage
-----

The plugin adds the following options to pytest::

    wish:
      --wish-specs=WISH_SPECS=[WISH_SPECS=...]
                            Space separated list of distribution specs, 'Python'
                            or 'all'.
      --wish-modules=WISH_MODULES=[WISH_MODULES=...]
                            Space separated list of module names.
      --wish-includes=WISH_INCLUDES=[WISH_INCLUDES=...]
                            Space separated list of regexs matching full object
                            names to include.
      --wish-excludes=WISH_EXCLUDES=[WISH_EXCLUDES=...]
                            Space separated list of regexs matching full object
                            names to exclude.
      --wish-predicate=WISH_PREDICATE
                            getmembers predicate full name, defaults to None.
      --wish-objects=WISH_OBJECTS
                            File of full object names to include.
      --wish-timeout=WISH_TIMEOUT
                            Test timeout.
      --wish-fail           Show wish failures.

Example usage, find a function that returns the factorial of a number::

    $ py.test examples/test_factorial.py --wish-modules math
    [...]
    examples/test_factorial.py::test_factorial[math:factorial] HIT
    [...]

the function ``factorial`` in the module ``math`` passes the ``test_factorial`` test.

Another example, find a function that decomposes a URL into individual rfc3986 components::

    $ py.test examples/test_rfc3986_parse.py --wish-modules urllib.parse
    [...]
    examples/test_rfc3986_parse.py::test_rfc3986_parse_basic[urllib.parse:urlparse] HIT
    examples/test_rfc3986_parse.py::test_rfc3986_parse_basic[urllib.parse:urlsplit] HIT
    [...]

the two functions ``urlparse`` and ``urlsplit`` pass the basic rfc3986 parsing test, but do not
pass the more complex ``test_rfc3986_parse_full`` test.

More advanced functions are available on PyPI::

    $ pip install urllib3
    $ py.test examples/test_rfc3986_parse.py --wish-modules urllib3
    [...]
    examples/test_rfc3986_parse.py::test_rfc3986_parse_basic[urllib3.util.url:parse_url] HIT
    examples/test_rfc3986_parse.py::test_rfc3986_parse_full[urllib3.util.url:parse_url] HIT
    [...]

now the function ``parse_url`` in the module ``urllib3.util.url`` passes both tests.


Help
----

We have the following support channels:

* `questions on stackoverflow`_
* `web-chat`_


Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

Contributors:

- Alessandro Amici - @alexamici

Sponsors:

.. image:: http://services.bopen.eu/bopen-logo.png
    :target: http://bopen.eu/
    :alt: B-Open Solutions srl


License
-------

Distributed under the terms of the `MIT`_ license, "pytest-wish" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`MIT`: http://opensource.org/licenses/MIT
.. _`file an issue`: https://github.com/alexamici/pytest-wish/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.org/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
.. _`@kr1`: https://github.com/kr1
.. _`questions on stackoverflow`: https://stackoverflow.com/search?q=pytest-wish
.. _`web-chat`: https://gitter.im/alexamici/pytest-wish

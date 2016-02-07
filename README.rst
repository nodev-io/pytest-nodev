pytest-wish
===========

.. image:: https://travis-ci.org/alexamici/pytest-wish.svg?branch=master
    :target: https://travis-ci.org/alexamici/pytest-wish
    :alt: Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/alexamici/pytest-wish?branch=master
    :target: https://ci.appveyor.com/project/alexamici/pytest-wish/branch/master
    :alt: Build Status on AppVeyor

.. image:: https://coveralls.io/repos/alexamici/pytest-wish/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/alexamici/pytest-wish
    :alt: Coverage Status on Coveralls


Search all installed modules for functions that pass a given feature-specification test suite.
See the `package documentation`_ for the gory details.

Intended audience: python developers who've got better things to do than reinvent wheels.

.. warning:: Development status: **almost beta** (but not quite there yet).


Source code *search by tests* or *Test-Driven no-Development*
-------------------------------------------------------------

    "Have a look at this piece of code that I’m writing--I’m sure it has been written before.
    I wouldn't be surprised to find it verbatim somewhere on GitHub." - `@kr1`_

`pytest-wish`_ is a `pytest`_ plugin that enables a software development strategy called
*search by tests* or *Test-Driven no-Development*,
that is an extension of the *Test-Driven Development* paradigm.

The idea is that once the developer has written the tests that define the behaviour of a new
function to a degree sufficient to validate the implementation they are going to write
it is good enough to validate
any implementation. Running the tests on a large set of functions may result in a *hit*, that is
a function that already implements their feature.

Due to its nature the approach is better suited for discovering smaller functions
with a generic signature.


Features
--------

* Runs a set of tests over all objects contained in a list of modules.


Requirements
------------

* TODO


Installation
------------

You can install `the latest version of "pytest-wish"`_ via the ``pip`` package manager::

    $ pip install pytest-wish


Usage
-----

The plugin adds the following options to pytest command line::

    wish:
      --wish-from-stdlib    Collects objects form the Python standard library.
      --wish-from-installed
                            Collects objects form all installed packages.
      --wish-from-all       Collects objects form the Python standard library and
                            all installed packages.
      --wish-from-specs=WISH_FROM_SPECS=[WISH_FROM_SPECS=...]
                            Collects objects from installed packages. Space
                            separated list of `pip` specs.
      --wish-from-modules=WISH_FROM_MODULES=[WISH_FROM_MODULES=...]
                            Collects objects from installed modules. Space
                            separated list of module names.
      --wish-includes=WISH_INCLUDES=[WISH_INCLUDES=...]
                            Space separated list of regexs matching full object
                            names to include, defaults to include all objects
                            collected via `--wish-from-*`.
      --wish-excludes=WISH_EXCLUDES=[WISH_EXCLUDES=...]
                            Space separated list of regexs matching full object
                            names to exclude, defaults to match 'internal use'
                            names '_|.*[.:]_'
      --wish-objects-from=WISH_OBJECTS_FROM
                            File name of full object names to include.
      --wish-predicate=WISH_PREDICATE
                            Full name of the predicate passed to
                            `inspect.getmembers`, defaults to `callable`.
      --wish-timeout=WISH_TIMEOUT
                            Test timeout.
      --wish-fail           Show wish failures.

Example usage, find a function that returns the factorial of a number::

    $ py.test examples/test_factorial.py --wish-from-modules math
    [...]
    examples/test_factorial.py::test_factorial[math:factorial] HIT
    [...]

the function ``factorial`` in the module ``math`` passes the ``test_factorial`` test.

Another example, find a function that decomposes a URL into individual rfc3986 components::

    $ py.test examples/test_rfc3986_parse.py --wish-from-modules urllib.parse
    [...]
    examples/test_rfc3986_parse.py::test_rfc3986_parse_basic[urllib.parse:urlparse] HIT
    examples/test_rfc3986_parse.py::test_rfc3986_parse_basic[urllib.parse:urlsplit] HIT
    [...]

the two functions ``urlparse`` and ``urlsplit`` pass the basic rfc3986 parsing test, but do not
pass the more complex ``test_rfc3986_parse_full`` test.

More advanced functions are available on PyPI::

    $ pip install urllib3
    $ py.test examples/test_rfc3986_parse.py --wish-from-modules urllib3
    [...]
    examples/test_rfc3986_parse.py::test_rfc3986_parse_basic[urllib3.util.url:parse_url] HIT
    examples/test_rfc3986_parse.py::test_rfc3986_parse_full[urllib3.util.url:parse_url] HIT
    [...]

now the function ``parse_url`` in the module ``urllib3.util.url`` passes both tests.


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

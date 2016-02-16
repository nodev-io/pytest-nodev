
User's Guide
============

.. warning:: This documentation is work in progress and there will be areas that are lacking.

Intended audience: python developers who've got better things to do than reinvent wheels.

Installation
------------

Install the `latest version of pytest-nodev <https://pypi.python.org/pypi/pytest-nodev>`_
from the Python Package Index::

    $ pip install pytest-nodev


Basic usage
-----------

Write a specification test instrumented with the ``wish`` fixture in the ``test_example.py`` file.
Run pytest with one of the ``--wish-from-*`` options to select the search space,
e.g. to search in the Python standard library::

    $ py.test --wish-from-stdlib test_example.py


Advanced usage
--------------

    $ py.test --wish-from-installed --wish-includes .*util -- test_example.py


Command line reference
----------------------

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


Examples
--------

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

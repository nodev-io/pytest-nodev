pytest-wish
===========

    "Have a look at this function that I'm writing...
    I'm sure someone else has already written it." - `@kr1`_

.. image:: https://travis-ci.org/alexamici/pytest-wish.svg?branch=master
    :target: https://travis-ci.org/alexamici/pytest-wish
    :alt: Build Status on Travis CI

.. image:: https://coveralls.io/repos/alexamici/pytest-wish/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/alexamici/pytest-wish
    :alt: Coverage Status on Coveralls

.. image:: https://badges.gitter.im/alexamici/pytest-wish.svg
    :target: https://gitter.im/alexamici/pytest-wish
    :alt: Join the chat at https://gitter.im/alexamici/pytest-wish

Test-Driven no-Development plugin for `pytest`_. The development status of this project is Alpha.

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
      --wish-dists=WISH_DISTS=[WISH_DISTS=...]
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
                            getmembers predicate full name, defaults to
                            'builtins:callable'.
      --wish-objects=WISH_OBJECTS
                            File of full object names to include.
      --wish-fail           Show wish failures.

Example usage, find a function that returns the factorial of a number::

    $ py.test -vv examples/test_factorial.py --wish-modules math | grep -v xfail$
    [...]
    examples/test_factorial.py::test_factorial[math:factorial] XPASS
    [...]

the function ``factorial`` in the module ``math`` passes the ``test_factorial`` test.

Another example, find a function that decomposes a URL into individual rfc3986 components::

    $ py.test -vv examples/test_rfc3986_parse.py --wish-modules urllib.parse | grep -v xfail$
    [...]
    examples/test_rfc3986_parse.py::test_rfc3986_parse_basic[urllib.parse:urlparse] XPASS
    examples/test_rfc3986_parse.py::test_rfc3986_parse_basic[urllib.parse:urlsplit] XPASS
    [...]

the two functions ``urlparse`` and ``urlsplit`` pass the basic rfc3986 parsing test, but do not
pass the more complex ``test_rfc3986_parse_full`` test.

More advanced functions are available on PyPI::

    $ pip install urllib3
    $ py.test -vv examples/test_rfc3986_parse.py --wish-modules urllib3 | grep -v xfail$
    [...]
    examples/test_rfc3986_parse.py::test_rfc3986_parse_basic[urllib3.util.url:parse_url] XPASS
    examples/test_rfc3986_parse.py::test_rfc3986_parse_full[urllib3.util.url:parse_url] XPASS
    [...]

now the function ``parse_url`` in the module ``urllib3.util.url`` passes both tests.


Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.


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

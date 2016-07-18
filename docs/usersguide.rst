
.. highlight:: console

User's guide
============

.. warning:: This section is work in progress and there will be areas that are lacking.

Installation
------------

Install the `latest version of pytest-nodev <https://pypi.python.org/pypi/pytest-nodev>`_
from the Python Package Index::

    $ pip install pytest-nodev


Basic usage
-----------

Write a specification test instrumented with the ``candidate`` fixture in the ``test_example.py`` file.
Run pytest with one of the ``--candidates-from-*`` options to select the search space,
e.g. to search in the Python standard library::

    $ py.test --candidates-from-stdlib test_example.py


Advanced usage
--------------

Use of ``--candidates-from-all`` may be very dangerous and it is disabled by default and
the preferred way to search safely and efficiently is documented in the :doc:`starterkit` section.

If you are sure you understand the risks and you have set up appropriate mitigation strategies
you can enable ``--candidates-from-all``
by setting the ``PYTEST_NODEV_MODE`` environment variable to ``FEARLESS``::

    $ PYTEST_NODEV_MODE=FEARLESS py.test --candidates-from-all test_example.py


Command line reference
----------------------

The plugin adds the following options to pytest command line::

    $ py.test --help
    [...]
    nodev:
      --candidates-from-stdlib
                            Collects candidates form the Python standard library.
      --candidates-from-all
                            Collects candidates form the Python standard library
                            and all installed packages. Disabled by default, see
                            the docs.
      --candidates-from-specs=CANDIDATES_FROM_SPECS=[CANDIDATES_FROM_SPECS=...]
                            Collects candidates from installed packages. Space
                            separated list of `pip` specs.
      --candidates-from-modules=CANDIDATES_FROM_MODULES=[CANDIDATES_FROM_MODULES=...]
                            Collects candidates from installed modules. Space
                            separated list of module names.
      --candidates-includes=CANDIDATES_INCLUDES=[CANDIDATES_INCLUDES=...]
                            Space separated list of regexs matching full object
                            names to include, defaults to include all objects
                            collected via `--candidates-from-*`.
      --candidates-excludes=CANDIDATES_EXCLUDES=[CANDIDATES_EXCLUDES=...]
                            Space separated list of regexs matching full object
                            names to exclude.
      --candidates-predicate=CANDIDATES_PREDICATE
                            Full name of the predicate passed to
                            `inspect.getmembers`, defaults to `builtins.callable`.
      --candidates-fail     Show candidates failures.
    [...]

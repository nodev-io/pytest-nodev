
.. warning:: Documentation status: **alpha**.

Getting Started
---------------


Installation
............

You can install `the latest version of "pytest-wish"`_ via the ``pip`` package manager::

    $ pip install pytest-wish


First test run
..............

Let's create a our first test file with the simple specification of the factorial function
using the ``wish`` fixture::

    # content of test_factoral.py
    def test_factorial(wish):
        factorial = wish
        assert factorial(0) == 1
        assert factorial(1) == 1
        assert factorial(21) == 51090942171709440000

That's it. You can now execute the test function on all functions in the Python standard library::

    $ py.test --wish-from-stdlib
    ======================= test session starts ==========================
    platform darwin -- Python 3.5.0, pytest-2.8.7, py-1.4.31, pluggy-0.3.1
    rootdir: /tmp, inifile: setup.cfg
    plugins: wish-0.9.0, timeout-1.0.0
    collected 3259 items

    test_factorial.py xxxxx[...]xxxxxXxxxxx[...]xxxxx

    ============================== 1 hit =================================

    test_factorial.py::test_factorial[math:factorial] HIT

    ==== 3258 xfailed, 1 xpassed, 27 pytest-warnings in 45.07 seconds ====

We just found that the ``factorial`` function in the ``math`` module is the only *HIT*,
that is it passes our specification test, and is the function we were looking for.


Usage
.....

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



.. _`the latest version of "pytest-wish"`: https://pypi.python.org/pypi/pytest-wish
.. _`pytest`: https://pytest.org

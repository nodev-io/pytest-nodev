
Design
======

This chapter documents the high-level design of the product and
it is intended for developers contributing to the project.

.. note:: **Users of the product need not bother with the following. Unless they are curious :)**


Mission and vision
------------------

The project mission is to enable test-driven code search for Python with pytest.

Target use cases:

#. test-driven reuse
#. tests validation

Project goals:

#. collect all possible python live objects (modules, functions, classes, singletons, constants...)
#. enable flexible search space definition
#. let users turn normal tests into specification tests, and vice versa, with minimal effort

Project non-goals:

#. protect the user from unintended consequences (clashes with goal 1.),
   instead document how to use OS-level isolation/containerization
#. help users writing implementation-independent specification tests
   (think a ``contains`` function that also tests inside dict values and class attributes)


Software architecture
---------------------

Logical components:

- the collector of candidate objects, with filtering
- the test runner, via the pytest plugin interface


Version goals
-------------

This project strives to adhere to `semantic versioning <http://semver.org>`_.


1.0.0 (upcoming release)
~~~~~~~~~~~~~~~~~~~~~~~~

Minimal set of features to be operationally useful and to showcase the nodev approach.
Reasonably safe to test, but not safe to use without OS-level isolation.
No completeness and no performance guarantees.

- Search environment definition:

  - Support defining which modules to search. Command line ``--candidates-from-*`` options.

  - Support defining which objects to include/exclude by name or via a predicate test function.
    Command line ``--candidates-includes/excludes/predicate`` options.

- Object collection:

  - Collect most objects from the defined environment. It is ok to miss some objects for now.

- Test execution:

  - Execute tests instrumented with the ``candidate`` fixture once for every object collected.
    The tests are marked ``xfail`` unless the ``--candidates-fail`` command line option is given to
    make standard pytest reporting the most useful.

- Report:

  - Report which objects pass each test.

- Safety:

  - Interrupting hanging tests is delegated to pytest-timeout.

  - Internal modules and objects starting with an underscore are excluded.

  - Potentially dangerous, crashing, hard hanging or simply annoying objects
    belonging to the standard library are unconditionally blacklisted
    so that new users can test ``--candidates-from-stdlib`` without bothering with OS-level isolation.

  - Limited use of ``--candidates-from-all``.

- Documentation:

  - Enough to inspire and raise interest in new users.

  - Enough to use it effectively and safely. Give a strategy to get OS-level isolation.


.. warning:: Documentation status: **alpha**.

Design
======


Mission and vision
------------------

The project mission is to enable searching live code by-tests with pytest.

Target use cases:

#. test-driven no-development
#. test validation

Goals:

#. collect all possible python live objects (modules, functions, classes, singletons, constants...)
#. enable flexible search space definition
#. enable change of normal tests to specification tests, and vice versa, with minimal effort

Non-goals:

#. protect the user from unintended consequences (clashes with goal 1.),
   instead simplify use of OS-level isolation/containerization
#. (may become a goal after 1.0 release) help users writing implementation-independent
   specification tests (think a ``contains`` function that also tests inside dict values and
   class attributes)


Software architecture
---------------------

Logical components:

- the collector
- the query
- pytest plugin interface
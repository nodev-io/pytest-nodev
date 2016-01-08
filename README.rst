pytest-wish
===========

.. image:: https://travis-ci.org/alexamici/pytest-wish.svg?branch=master
    :target: https://travis-ci.org/alexamici/pytest-wish
    :alt: Build Status on Travis CI

.. image:: https://coveralls.io/repos/alexamici/pytest-wish/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/alexamici/pytest-wish
    :alt: Coverage Status on Coveralls

Test-Driven no-Development plugin for `pytest`_. The development status of this project is early Alpha.

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

Example usage:

    $ py.test -vv examples/ --wish-modules math | grep -v xfail$
    [...]
    examples/test_factoral.py::test_factorial[math:factorial] XPASS
    [...]

the function `factorial` in the module `math` passes the `test_factorial` test.

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

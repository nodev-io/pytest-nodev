
.. highlight:: console

This project is Free and Open Source Software released under the terms of the
`MIT license <http://opensource.org/licenses/MIT>`_.
Contributions are highly welcomed and appreciated. Every little help counts, so do not hesitate!


Report a bug
------------

If you encounter any problems, please file a bug report
in the project `issue tracker <https://github.com/nodev-io/pytest-nodev/issues>`_
along with a detailed description.


Submit a pull request
---------------------

Contributors are invited to review the
`product high level design <https://pytest-nodev.readthedocs.io/en/latest/design.html>`_
and the `short term product planning <https://github.com/nodev-io/pytest-nodev/milestones>`_.

Tests can be run with `pytest <https://pytest.org>`_ with::

    $ py.test -v --timeout=0 --pep8 --flakes --mccabe --cov=pytest_nodev --cov-report=html \
        --cache-clear pytest_nodev tests

coverage is can be checked with::

    $ open htmlcov/index.html

the complete python versions tests can be run via `tox <https://tox.readthedocs.io>`_ with::

    $ tox

Please ensure the coverage at least stays the same before you submit a pull request.


Documentation
-------------

The documentation is in `reStructuredText <http://www.sphinx-doc.org/en/stable/rest.html>`_ format,
you can build a local copy with::

    $ sphinx-build docs docs/html
    $ open docs/html/index.html

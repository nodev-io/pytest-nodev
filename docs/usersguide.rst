
User's guide
============

.. warning:: This section is work in progress and there will be areas that are lacking.

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

Use of ``--wish-from-all`` may be very dangerous
and it is disabled by default.

In order to search safely in all modules we suggest to use docker for OS-level isolation.
To kickstart your advanced usage downlaod the nodev-tutorial::

    $ git clone https://github.com/nodev-io/nodev-tutorial.git
    $ cd nodev-tutorial

build the nodev docker image with all module from requirements.txt installed::

    $ docker build -t nodev .

and run tests with::

    $ docker run --rm -it -v `pwd`:/home/pytest nodev --wish-from-all tests/test_factorial.py

Alternatively you can enable it on your regular user only after you have understood the risks
and set up appropriate mitigation strategies
by setting the ``PYTEST_NODEV_MODE`` environment variable to ``FEARLESS``::

    $ PYTEST_NODEV_MODE=FEARLESS py.test --wish-from-all --wish-includes .*util -- test_example.py


Command line reference
----------------------

The plugin adds the following options to pytest command line::

    wish:
      --wish-from-stdlib    Collects objects form the Python standard library.
      --wish-from-all       Collects objects form the Python standard library and
                            all installed packages. Disabled by default, see the
                            docs.
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
                            names to exclude.
      --wish-predicate=WISH_PREDICATE
                            Full name of the predicate passed to
                            `inspect.getmembers`, defaults to `builtins.callable`.
      --wish-fail           Show wish failures.


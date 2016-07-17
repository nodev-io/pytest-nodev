
1.0.0 (2016-07-18)
------------------

- Mostly documentation updates. The documentation is promoted to *good enough*.
  Issue `#17 <https://github.com/nodev-io/pytest-nodev/issues/17>`_.


0.9.9 (2016-07-16)
------------------

- Reduce test run noise by blacklisting annoying stdlib objects.
  Issue `#12 <https://github.com/nodev-io/pytest-nodev/issues/12>`_.
- Report object that pass a test as **PASSED**, phase out HIT concept altogether.
- Get docs and dependencies in shape for the 1.0.0 release.


0.9.8 (2016-03-16)
------------------

- Add the ``pytest.mark.candidate`` marker in the place of ``pytest_nodev.search``.
  Issue `#28 <https://github.com/nodev-io/pytest-nodev/issues/28>`_.
- Rename main fixture to ``candidate`` from ``wish``.
  Issue `#30 <https://github.com/nodev-io/pytest-nodev/issues/30>`_.
  So long, and thanks for all the fish.


0.9.7 (2016-03-13)
------------------

- Add the ``pytest_nodev.search`` decorator for simpler test instrumentation.
  Issue `#19 <https://github.com/nodev-io/pytest-nodev/issues/19>`_.


0.9.6 (2016-03-06)
------------------

- Mostly documentation improvements and fixes.


0.9.5 (2016-03-01)
------------------

- Really find all installed modules thanks to a better sub-module discovery logic for packages.
  Issue `#2 <https://github.com/nodev-io/pytest-nodev/issues/2>`_.
- Drop stdlib-list and its bloated dependency tree,
  issue `#23 <https://github.com/nodev-io/pytest-nodev/issues/23>`_.


0.9.4 (2016-02-28)
------------------

- Fixed the frequent "AssertionError: Silent re.match bug!",
  issue `#24 <https://github.com/nodev-io/pytest-nodev/issues/24>`_.
- Added more problem objects to the blacklist.


0.9.3 (2016-02-25)
------------------

- Simplified command line interface.
- Added docs on how to run inside a docker container.
- Bug-fixes and performance improvements.


0.9.2 (2016-02-20)
------------------

- Disable potentially dangerous ``--candidates-from-all`` by default.


0.9.1 (2016-02-16)
------------------

- Rename the project to pytest-nodev (was pytest-wish).


0.9.0 (2016-02-14)
------------------

- First beta release.

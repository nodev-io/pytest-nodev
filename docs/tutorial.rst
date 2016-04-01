
Tutorial
========

.. warning:: This section is work in progress and there will be areas that are lacking.

Starter kit
-----------

Use of ``--candidates-from-all`` may be very dangerous
and it is disabled by default.

In order to search safely in all modules we suggest to use docker for OS-level isolation.
To kickstart your advanced usage download the nodev-starter-kit::

    $ git clone https://github.com/nodev-io/nodev-starter-kit.git
    $ cd nodev-starter-kit

build the nodev docker image with all module from requirements.txt installed::

    $ docker build -t nodev .

and run tests with::

    $ docker run --rm -it -v `pwd`:/home/pytest nodev --candidates-from-all tests/test_factorial.py

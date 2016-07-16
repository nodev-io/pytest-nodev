
Tutorial
========

.. warning:: This section is work in progress and there will be areas that are lacking.

nodev starter kit
-----------------

Use of ``--candidates-from-all`` may be very dangerous
and it is disabled by default.

In order to search safely in all modules we suggest to use docker for OS-level isolation.

To kickstart your advanced usage clone the nodev-starter-kit::

    $ git clone https://github.com/nodev-io/nodev-starter-kit.git

or better yet, fork it on GitHub and clone your own fork::

    $ git clone https://github.com/YOUR_GITHUB_NAME/nodev-starter-kit.git

Enter the starter kit folder::

    $ cd nodev-starter-kit

build the nodev docker image with all module from requirements.txt installed::

    $ docker build -t nodev .

and run tests with::

    $ docker run --rm -it -v `pwd`:/home/pytest nodev --candidates-from-all tests/test_factorial.py


.. highlight:: console

Starter kit
===========

**nodev-starter-kit** lets you perform test-driven code search queries
with `pytest-nodev <https://pypi.python.org/pypi/pytest-nodev>`_
safely and efficiently using `docker <https://docker.com>`_.

**Why do I need special care to run pytest-nodev?**

Searching code with pytest-nodev looks very much like running arbitrary callables with random arguments.
A lot of functions called with the wrong set of arguments may have unexpected consequences ranging
from slightly annoying, think ``os.mkdir('false')``,
to **utterly catastrophic**, think ``shutil.rmtree('/', True)``.
Serious use of pytest-nodev, in particular using ``--candidates-from-all``,
require running the tests with operating-system level isolation,
e.g. as a dedicated user or even better inside a dedicated container.

**But isn't it docker overkill? Can't I just use a dedicated user to run pytest-nodev?**

We tried hard to find a simpler setup, but once all the nitty-gritty details are factored in
we choose docker as the best trade-off between safety, reproducibility and easiness of use.


Install nodev-starter-kit
-------------------------

To install *nodev-starter-kit* clone the `official repo <https://github.com/nodev-io/nodev-startet-kit>`_::

    $ git clone https://github.com/nodev-io/nodev-starter-kit.git
    $ cd nodev-starter-kit

Advanced GitHub users are suggested to
`fork the offical repo <https://help.github.com/articles/fork-a-repo/>`_ and clone their fork.


Install docker-engine and docker
--------------------------------

In order to run pytest-nodev you need to access a docker-engine server via the docker client,
if you don't have Docker already setup
you need to follow the official installation instructions for your platform:

- `Docker for Linux <https://docs.docker.com/engine/installation/linux/>`_
- `Docker for MacOS <https://docs.docker.com/docker-for-mac/>`_
- `Docker for Windows <https://docs.docker.com/docker-for-windows/>`_

Only on Ubuntu 16.04 you can use the script we provide::

    $ bash ./docker-engine-setup.sh

And test your setup with::

    $ docker info

Refer to the official Docker documentation for trouble-shooting and additional configurations.


Create the nodev image
----------------------

The *nodev* docker image will be your search engine,
it needs to be created once and updated every time you want to
change the packages installed in the search engine environment.

With an editor fill the requirements.txt file with the packages to be installed in the search engine.

Build the docker image with::

    $ docker build -t nodev .


Execute a search
----------------

Run the search engine container on a local docker-engine server, e.g. with::

    $ docker run --rm -it -v `pwd`:/src nodev --candidates-from-stdlib tests/test_parse_bool.py

Or alternatively after having set the ``DOCKER_HOST`` environment variable, e.g. with::

    $ export DOCKER_HOST='tcp://127.0.0.1:4243'  # change '127.0.0.1:4243' with the IP address and port
                                                 # of your remote docker-engine host

you can run the search engine container on a remote docker-engine server, e.g. with::

    $ python docker-nodev.py --candidates-from-stdlib tests/test_parse_bool.py
    ======================= test session starts ==========================
    platform darwin -- Python 3.5.1, pytest-2.9.2, py-1.4.31, pluggy-0.3.1
    rootdir: /tmp, inifile: setup.cfg
    plugins: nodev-1.0.0, timeout-1.0.0
    collected 4000 items

    test_parse_bool.py xxxxxxxxxxxx[...]xxxxxxxxXxxxxxxxx[...]xxxxxxxxxxxx

    ====================== pytest_nodev: 1 passed ========================

    test_parse_bool.py::test_parse_bool[distutils.util:strtobool] PASSED

    === 3999 xfailed, 1 xpassed, 260 pytest-warnings in 75.38 seconds ====

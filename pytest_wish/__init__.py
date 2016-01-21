# -*- coding: utf-8 -*-

# python 2 support via python-future
from __future__ import absolute_import, unicode_literals
from builtins import dict, super, zip

import argparse
import logging
import sys

import pytest

from pytest_wish import utils


def pytest_addoption(parser):
    group = parser.getgroup('wish')
    group.addoption('--wish-dists', default=[], nargs='+',
                    help="Space separated list of distribution specs, 'Python' or 'all'.")
    group.addoption('--wish-modules', default=[], nargs='+',
                    help="Space separated list of module names.")
    group.addoption('--wish-includes', nargs='+',
                    help="Space separated list of regexs matching full object names to include.")
    group.addoption('--wish-excludes', default=utils.EXCLUDE_PATTERNS, nargs='+',
                    help="Space separated list of regexs matching full object names to exclude.")
    group.addoption('--wish-objects', type=argparse.FileType('r'),
                    help="File of full object names to include.")
    group.addoption('--wish-fail', action='store_true', help="Show wish failures.")


class PytestHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET, config=None):
        super(PytestHandler, self).__init__(level=level)
        self._emit = config._warn

    def emit(self, record):
        self._emit(self.format(record))


def pytest_configure(config):
    # take over utils logging
    utils.logger.propagate = False
    utils.logger.setLevel(logging.DEBUG)  # FIXME: loglevel should be configurable
    utils.logger.addHandler(PytestHandler(config=config))


def pytest_generate_tests(metafunc):
    if 'wish' not in metafunc.fixturenames:
        return

    wish_dists = metafunc.config.getoption('wish_dists')
    utils.import_distributions(wish_dists)

    wish_modules = metafunc.config.getoption('wish_modules')
    utils.import_modules(wish_modules)

    wish_includes = metafunc.config.getoption('wish_includes') or wish_modules
    wish_excludes = metafunc.config.getoption('wish_excludes')

    # NOTE: 'copy' is needed here because indexing may unexpectedly trigger a module load
    object_index = dict(
        utils.generate_objects_from_modules(sys.modules.copy(), wish_includes, wish_excludes)
    )

    wish_objects = metafunc.config.getoption('wish_objects')
    if wish_objects is not None:
        object_index.update(utils.generate_objects_from_names(wish_objects))

    ids, params = list(zip(*sorted(object_index.items()))) or [(), ()]
    metafunc.parametrize('wish', params, ids=ids, scope='module')

    wish_fail = metafunc.config.getoption('wish_fail')
    if not wish_fail:
        metafunc.function = pytest.mark.xfail(metafunc.function)

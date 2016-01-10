# -*- coding: utf-8 -*-

import argparse
import sys

import pytest

from pytest_wish import utils


def pytest_addoption(parser):
    group = parser.getgroup('wish')
    group.addoption('--wish-modules', default=(), nargs='+',
                    help="Space separated list of module names.")
    group.addoption('--wish-includes', nargs='+',
                    help="Space separated list of regexs matching full object names to include.")
    # enable support for '--wish-includes all'
    utils.ENABLE_IMPORT_ALL = True
    group.addoption('--wish-excludes', default=(), nargs='+',
                    help="Space separated list of regexs matching full object names to exclude.")
    group.addoption('--wish-objects', type=argparse.FileType('r'),
                    help="File of full object names to include.")
    group.addoption('--wish-fail', action='store_true', help="Show wish failures.")


def pytest_generate_tests(metafunc):
    if 'wish' not in metafunc.fixturenames:
        return

    wish_modules = metafunc.config.getoption('wish_modules')
    utils.import_modules(wish_modules)

    wish_includes = metafunc.config.getoption('wish_includes') or wish_modules
    wish_excludes = metafunc.config.getoption('wish_excludes')

    # NOTE: 'copy' is needed here because index_modules may unexpectedly trigger a module load
    object_index = utils.index_modules(sys.modules.copy(), wish_includes, wish_excludes)

    wish_objects = metafunc.config.getoption('wish_objects')
    if wish_objects is not None:
        object_index.update(utils.index_objects(wish_objects))

    ids, params = list(zip(*sorted(object_index.items()))) or [(), ()]
    metafunc.parametrize('wish', params, ids=ids, scope='module')

    wish_fail = metafunc.config.getoption('wish_fail')
    if not wish_fail:
        metafunc.function = pytest.mark.xfail(metafunc.function)

# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2016 Alessandro Amici
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

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
    group.addoption('--wish-specs', default=[], nargs='+',
                    help="Space separated list of distribution specs, 'Python' or 'all'.")
    group.addoption('--wish-modules', default=[], nargs='+',
                    help="Space separated list of module names.")
    group.addoption('--wish-includes', nargs='+',
                    help="Space separated list of regexs matching full object names to include.")
    group.addoption('--wish-excludes', default=utils.EXCLUDE_PATTERNS, nargs='+',
                    help="Space separated list of regexs matching full object names to exclude.")
    group.addoption('--wish-predicate',
                    help="getmembers predicate full name, defaults to None.")
    group.addoption('--wish-objects', type=argparse.FileType('r'),
                    help="File of full object names to include.")
    group.addoption('--wish-timeout', default=1, help="Test timeout.")
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

    # build the object index
    wish_specs = config.getoption('wish_specs')
    utils.import_distributions(wish_specs)

    wish_modules = config.getoption('wish_modules')
    utils.import_modules(wish_modules)

    wish_includes = config.getoption('wish_includes') or wish_modules
    wish_excludes = config.getoption('wish_excludes')
    wish_predicate = config.getoption('wish_predicate')

    # NOTE: 'copy' is needed here because indexing may unexpectedly trigger a module load
    modules = sys.modules.copy()
    object_index = dict(
        utils.generate_objects_from_modules(modules, wish_includes, wish_excludes, wish_predicate)
    )

    wish_objects = config.getoption('wish_objects')
    if wish_objects is not None:
        object_index.update(utils.generate_objects_from_names(wish_objects))

    # store options
    config._wish_index_items = list(zip(*sorted(object_index.items()))) or [(), ()]
    config._wish_timeout = config.getoption('wish_timeout')
    config._wish_fail = config.getoption('wish_fail')


def pytest_generate_tests(metafunc):
    if 'wish' not in metafunc.fixturenames:
        return

    ids, params = metafunc.config._wish_index_items
    metafunc.parametrize('wish', params, ids=ids, scope='module')
    metafunc.function = pytest.mark.timeout(metafunc.config._wish_timeout)(metafunc.function)
    if not metafunc.config._wish_fail:
        metafunc.function = pytest.mark.xfail(metafunc.function)

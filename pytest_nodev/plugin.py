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
from builtins import dict, list, zip

import collections
import inspect
import logging
import os
import sys

import pytest

from . import collect
from . import utils


def pytest_addoption(parser):
    group = parser.getgroup('nodev')
    group.addoption(
        '--candidates-from-stdlib', action='store_true',
        help="Collects candidates form the Python standard library.")
    group.addoption(
        '--candidates-from-all', action='store_true',
        help="Collects candidates form the Python standard library and all installed packages. "
             "Disabled by default, see the docs.")
    group.addoption(
        '--candidates-from-specs', default=[], nargs='+',
        help="Collects candidates from installed packages. Space separated list of `pip` specs.")
    group.addoption(
        '--candidates-from-modules', default=[], nargs='+',
        help="Collects candidates from installed modules. Space separated list of module names.")
    group.addoption(
        '--candidates-includes', nargs='+',
        help="Space separated list of regexs matching full object names to include, "
             "defaults to include all objects collected via `--candidates-from-*`.")
    group.addoption(
        '--candidates-excludes', default=[], nargs='+',
        help="Space separated list of regexs matching full object names to exclude.")
    group.addoption(
        '--candidates-predicate', default='builtins:callable',
        help="Full name of the predicate passed to `inspect.getmembers`, "
             "defaults to `builtins.callable`.")
    group.addoption('--candidates-fail', action='store_true', help="Show candidates failures.")


def make_candidate_index(config):
    if config.getoption('candidates_from_all') and os.environ.get('PYTEST_NODEV_MODE') != 'FEARLESS':
        raise ValueError("Use of --candidates-from-all may be very dangerous, see the docs.")

    if not hasattr(config, '_candidate_index'):
        # take over collect logging
        collect.logger.propagate = False
        collect.logger.setLevel(logging.DEBUG)  # FIXME: loglevel should be configurable
        collect.logger.addHandler(utils.EmitHandler(config._warn))

        # delegate interrupting hanging tests to pytest-timeout
        os.environ['PYTEST_TIMEOUT'] = os.environ.get('PYTEST_TIMEOUT', '1')

        # build the object index
        distributions = collections.OrderedDict()

        if config.getoption('candidates_from_stdlib') or config.getoption('candidates_from_all'):
            distributions.update(collect.collect_stdlib_distributions())

        if config.getoption('candidates_from_all'):
            distributions.update(collect.collect_installed_distributions())

        distributions.update(collect.collect_distributions(config.getoption('candidates_from_specs')))

        if config.getoption('candidates_from_modules'):
            distributions['unknown distribution'] = config.getoption('candidates_from_modules')

        top_level_modules = collect.import_distributions(distributions.items())

        includes = config.getoption('candidates_includes')
        if not includes:
            includes = ['.'] if config.getoption('candidates_from_all') else sorted(top_level_modules)
        excludes = config.getoption('candidates_excludes')
        predicate = config.getoption('candidates_predicate')

        # NOTE: 'copy' is needed here because indexing may unexpectedly trigger a module load
        modules = sys.modules.copy()
        object_index = dict(
            collect.generate_objects_from_modules(modules, includes, excludes, predicate)
        )

        # store index
        config._candidate_index = list(zip(*sorted(object_index.items()))) or [(), ()]

    return config._candidate_index


def pytest_pycollect_makeitem(collector, name, obj):
    candidate_marker = getattr(obj, 'candidate', None)
    if candidate_marker and getattr(candidate_marker, 'args', []):
        candidate_name = candidate_marker.args[0]

        def wrapper(candidate, monkeypatch, *args, **kwargs):
            if '.' in candidate_name:
                monkeypatch.setattr(candidate_name, candidate, raising=False)
            else:
                monkeypatch.setattr(inspect.getmodule(obj), candidate_name, candidate, raising=False)
            return obj(*args, **kwargs)

        wrapper.__dict__ = obj.__dict__
        return list(collector._genfunctions(name, wrapper))


def pytest_generate_tests(metafunc):
    if 'candidate' not in metafunc.fixturenames:
        return

    ids, params = make_candidate_index(metafunc.config)
    metafunc.parametrize('candidate', params, ids=ids, scope='module')

    if not metafunc.config.getoption('candidates_fail'):
        metafunc.function = pytest.mark.xfail(metafunc.function)


def pytest_terminal_summary(terminalreporter):
    if not hasattr(terminalreporter.config, '_candidate_index'):
        return

    passed_state = 'passed' if terminalreporter.config.getoption('candidates_fail') else 'xpassed'
    passed_reports = terminalreporter.getreports(passed_state)
    terminalreporter.write_sep('=', 'pytest_nodev: %d passed' % len(passed_reports), bold=True)
    terminalreporter.write_line('')
    for report in passed_reports:
        terminalreporter.write(report.nodeid)
        terminalreporter.write_line(' PASSED', bold=True, green=True)
    terminalreporter.write_line('')

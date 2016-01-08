# -*- coding: utf-8 -*-

import importlib
import inspect
import re
import sys

import pkg_resources
import pytest


BLACKLIST = pkg_resources.resource_string('pytest_wish', 'wish_blacklist.txt').decode('utf-8').splitlines()


def pytest_addoption(parser):
    group = parser.getgroup('wish')
    group.addoption('--wish-modules', default=(), nargs='+',
                    help="Space separated list of module names.")
    group.addoption('--wish-includes', nargs='+',
                    help="Space separated list of regexs matching full object names to include.")
    group.addoption('--wish-excludes', default=(), nargs='+',
                    help="Space separated list of regexs matching full object names to exclude.")
    group.addoption('--wish-fail', action='store_true', help="Show wish failures.")


def generate_module_objects(module):
    try:
        module_members = inspect.getmembers(module)
    except ImportError:
        raise StopIteration
    for object_name, object_ in module_members:
        if inspect.getmodule(object_) is module:
            yield object_name, object_


def valid_name(name, include_res, exclude_res):
    include_name = any(include_re.match(name) for include_re in include_res)
    exclude_name = any(exclude_re.match(name) for exclude_re in exclude_res)
    return include_name and not exclude_name


def index_modules(modules, include_patterns, exclude_patterns=(), blacklist=BLACKLIST):
    exclude_patterns += tuple(name.strip() + '$' for name in BLACKLIST)
    include_res = [re.compile(pattern) for pattern in include_patterns]
    exclude_res = [re.compile(pattern) for pattern in exclude_patterns]
    object_index = {}
    for module_name, module in modules.items():
        for object_name, object_ in generate_module_objects(module):
            full_object_name = '{}:{}'.format(module_name, object_name)
            if valid_name(full_object_name, include_res, exclude_res):
                object_index[full_object_name] = object_
    return object_index


def pytest_generate_tests(metafunc):
    if 'wish' not in metafunc.fixturenames:
        return

    wish_modules = metafunc.config.getoption('wish_modules')
    for module_name in wish_modules:
        importlib.import_module(module_name)

    wish_includes = metafunc.config.getoption('wish_includes') or wish_modules
    wish_excludes = metafunc.config.getoption('wish_excludes')

    # NOTE: 'copy' is needed here because index_modules may unexpectedly trigger a module load
    object_index = index_modules(sys.modules.copy(), wish_includes, wish_excludes)
    object_items = sorted(object_index.items())
    ids, params = list(zip(*object_items)) or [[], []]
    metafunc.parametrize('wish', params, ids=ids, scope='module')

    wish_fail = metafunc.config.getoption('wish_fail')
    if not wish_fail:
        metafunc.function = pytest.mark.xfail(metafunc.function)

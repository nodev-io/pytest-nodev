# -*- coding: utf-8 -*-

import importlib
import inspect
import re
import sys

import pytest


def pytest_addoption(parser):
    group = parser.getgroup('wish')
    group.addoption('--wish-modules', default=(), nargs='+',
                    help="Space separated list of module names.")
    group.addoption('--wish-includes', nargs='+',
                    help="Space separed list of regex of fully qualified object names to include.")
    group.addoption('--wish-fail', action='store_true', help="Show wish failures.")


def generate_module_objects(module):
    for obj_name, obj in inspect.getmembers(module):
        if obj_name.startswith('__'):
            continue
        obj_module = inspect.getmodule(obj)
        if obj_module is not module:
            continue
        yield obj_name, obj


def index_modules(modules, include_regexs):
    include_res = [re.compile(regex) for regex in include_regexs]
    object_index = {}
    for module_name, module in modules.items():
        for object_name, object_ in generate_module_objects(module):
            fully_qualified_object_name = '{}:{}'.format(module_name, object_name)
            for include_re in include_res:
                if include_re.match(fully_qualified_object_name):
                    object_index[fully_qualified_object_name] = object_
                    break
    return object_index


def pytest_generate_tests(metafunc):
    if 'wish' not in metafunc.fixturenames:
        return

    wish_modules = metafunc.config.getoption('wish_modules')
    for module_name in wish_modules:
        importlib.import_module(module_name)

    wish_includes = metafunc.config.getoption('wish_includes') or wish_modules
    # NOTE: 'copy' is needed here because index_modules may unexpectedly trigger a module load
    object_index = index_modules(sys.modules.copy(), tuple(wish_includes))
    object_items = sorted(object_index.items())
    ids, params = list(zip(*object_items)) or [[], []]
    metafunc.parametrize('wish', params, ids=ids, scope='module')

    wish_fail = metafunc.config.getoption('wish_fail')
    if not wish_fail:
        metafunc.function = pytest.mark.xfail(metafunc.function)

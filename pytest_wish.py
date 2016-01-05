# -*- coding: utf-8 -*-
from __future__ import print_function

import importlib
import inspect

import pytest


def pytest_addoption(parser):
    group = parser.getgroup('wish')
    group.addoption('--wish-modules', default='', help="Comma separated list of module names.")
    group.addoption('--wish-fail', action='store_true', help="Show wish failures.")


def pytest_generate_tests(metafunc):
    if 'wish' not in metafunc.fixturenames:
        return
    wish_modules = metafunc.config.getoption('wish_modules')
    wish_fail = metafunc.config.getoption('wish_fail')
    module_names = wish_modules.split(',') if wish_modules else []
    object_index = {}
    for module_name in module_names:
        module = importlib.import_module(module_name)
        for obj_name, obj in inspect.getmembers(module):
            if obj_name.startswith('__'):
                continue
            obj_module = inspect.getmodule(obj)
            if obj_module is not module:
                continue
            object_index[obj_name] = obj
    object_items = sorted(object_index.items())
    ids, params = list(zip(*object_items)) or [[], []]
    metafunc.parametrize('wish', params, ids=ids, scope='module')
    if not wish_fail:
        metafunc.function = pytest.mark.xfail(metafunc.function)

# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2016 Alessandro Amici
#

import pytest

from pytest_wish import blacklists
from pytest_wish import collect


def test_import_coverage():
    """Fix the coverage by pytest-cov, that may trigger after pytest_wish is already imported."""
    from imp import reload  # Python 2 and 3 reload
    reload(blacklists)
    reload(collect)


def test_collect_stdlib_distributions():
    stdlib_distributions = list(collect.collect_stdlib_distributions())
    assert len(stdlib_distributions) == 1
    _, module_names = stdlib_distributions[0]
    assert len(module_names) > 10


def test_collect_installed_distributions():
    installed_distributions = list(collect.collect_installed_distributions())
    assert len(installed_distributions) > 1
    for spec, module_names in installed_distributions:
        if spec.startswith('pytest-wish'):
            break
    assert module_names == ['pytest_wish']


def test_collect_distributions():
    distributions = list(collect.collect_distributions(['pytest-wish']))
    assert len(distributions) == 1
    _, module_names = distributions[0]
    assert len(module_names) == 1
    assert len(list(collect.collect_distributions(['non_existent_distribution']))) == 0


def test_import_module():
    assert collect.import_module('pytest_wish')
    with pytest.raises(ImportError):
        collect.import_module('pytest_wish', module_blacklist_pattern='pytest_wish')
    with pytest.raises(ImportError):
        collect.import_module('non_existent_module')


def test_import_distributions():
    distributions = [('pytest-wish', ['pytest_wish'])]
    module_names = list(collect.import_distributions(distributions))
    assert module_names == ['pytest_wish']

    distributions = [('pytest-wish', ['non_existent_module'])]
    module_names = list(collect.import_distributions(distributions))
    assert module_names == []


def test_generate_module_objects():
    expected_item = ('generate_module_objects', collect.generate_module_objects)
    assert expected_item in list(collect.generate_module_objects(collect))


def test_generate_objects_from_modules():
    import re
    modules = {'pytest_wish.collection': collect, 're': re}
    include_patterns = ['pytest_wish.collection:generate_objects_from_modules']
    objs = collect.generate_objects_from_modules(
        modules, include_patterns, module_blacklist_pattern='re')
    assert len(list(objs)) == 1


def test_object_from_name():
    object_ = collect.object_from_name('pytest_wish.collect:object_from_name')
    assert object_ == collect.object_from_name


def test_generate_objects_from_names():
    # normal path
    names = ['pytest_wish.collect:generate_objects_from_names']
    assert len(list(collect.generate_objects_from_names(names))) == 1
    # error paths
    names = ['# comment', 'non_existent_module:', 'math:non_existent_object']
    assert len(list(collect.generate_objects_from_names(names))) == 0

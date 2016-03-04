# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2016 Alessandro Amici
#

# python 2 support via python-future
from __future__ import absolute_import, unicode_literals
from builtins import list

import pytest

from pytest_nodev import blacklists
from pytest_nodev import collect


def test_import_coverage():
    """Fix the coverage by pytest-cov, that may trigger after pytest_nodev is already imported."""
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
        if spec.startswith('pytest-nodev'):
            break
    assert module_names == ['pytest_nodev']


def test_collect_distributions():
    distributions = list(collect.collect_distributions(['pytest-nodev']))
    assert len(distributions) == 1
    _, module_names = distributions[0]
    assert len(module_names) == 1
    assert len(list(collect.collect_distributions(['non_existent_distribution']))) == 0


def test_import_module():
    assert collect.import_module('pytest_nodev')
    with pytest.raises(ImportError):
        collect.import_module('pytest_nodev', module_blacklist_pattern='pytest_nodev')
    with pytest.raises(ImportError):
        collect.import_module('non_existent_module')


def test_import_distributions():
    distributions = [('pytest-nodev', ['pytest_nodev'])]
    module_names = list(collect.import_distributions(distributions))
    assert module_names == ['pytest_nodev']

    distributions = [('pytest-nodev', ['non_existent_module'])]
    module_names = list(collect.import_distributions(distributions))
    assert module_names == []


def test_generate_module_objects():
    expected_item = ('generate_module_objects', collect.generate_module_objects)
    assert expected_item in list(collect.generate_module_objects(collect))


def test_generate_objects_from_modules():
    import re
    modules = {'pytest_nodev.collection': collect, 're': re}
    include_patterns = ['pytest_nodev.collection:generate_objects_from_modules']
    objs = collect.generate_objects_from_modules(
        modules, include_patterns, module_blacklist_pattern='re')
    assert len(list(objs)) == 1


def test_object_from_name():
    object_ = collect.object_from_name('pytest_nodev.collect:object_from_name')
    assert object_ is collect.object_from_name

    # instance methods compare by equality, see http://stackoverflow.com/questions/15977808
    object_ = collect.object_from_name('pytest_nodev.collect:NOMATCH_PATTERN.upper')
    assert object_ == collect.NOMATCH_PATTERN.upper

# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2016 Alessandro Amici
#

import pytest

from pytest_wish import utils


def test_import_coverage():
    """Fix the coverage by pytest-cov, that may trigger after pytest_wish is already imported."""
    from imp import reload  # Python 2 and 3 reload
    reload(utils)


def test_collect_stdlib_distributions():
    stdlib_distributions = list(utils.collect_stdlib_distributions())
    assert len(stdlib_distributions) == 1
    _, module_names = stdlib_distributions[0]
    assert len(module_names) > 10


def test_collect_installed_distributions():
    installed_distributions = list(utils.collect_installed_distributions())
    assert len(installed_distributions) > 1
    for spec, module_names in installed_distributions:
        if spec.startswith('pytest-wish'):
            break
    assert module_names == ['pytest_wish']


def test_collect_distributions():
    distributions = list(utils.collect_distributions(['pytest-wish']))
    assert len(distributions) == 1
    _, module_names = distributions[0]
    assert len(module_names) == 1
    assert len(list(utils.collect_distributions(['non_existent_distribution']))) == 0


def test_valid_name():
    assert utils.valid_name('math:factorial')

    assert utils.valid_name('math:factorial', include_pattern='math')
    assert utils.valid_name('math:factorial', include_pattern='.*:factorial$')
    assert not utils.valid_name('math:factorial', include_pattern='abc')

    assert not utils.valid_name('math:factorial', exclude_pattern='math')
    assert not utils.valid_name('math:factorial', exclude_pattern='.*:factorial$')
    assert utils.valid_name('math:factorial', exclude_pattern='abc')

    assert utils.valid_name('math:factorial', include_pattern='m', exclude_pattern='moo')
    assert not utils.valid_name('math:factorial', include_pattern='m', exclude_pattern='math')


def test_import_module():
    assert utils.import_module('pytest_wish')
    with pytest.raises(ImportError):
        utils.import_module('pytest_wish', module_blacklist_pattern='pytest_wish')
    with pytest.raises(ImportError):
        utils.import_module('non_existent_module')


def test_import_distributions():
    distributions = [('pytest-wish', ['pytest_wish'])]
    module_names = list(utils.import_distributions(distributions))
    assert module_names == ['pytest_wish']

    distributions = [('pytest-wish', ['non_existent_module'])]
    module_names = list(utils.import_distributions(distributions))
    assert module_names == []


def test_generate_module_objects():
    expected_item = ('generate_module_objects', utils.generate_module_objects)
    assert expected_item in list(utils.generate_module_objects(utils))


def test_generate_objects_from_modules():
    import re
    modules = {'pytest_wish.utils': utils, 're': re}
    include_patterns = ['pytest_wish.utils:generate_objects_from_modules']
    objs = utils.generate_objects_from_modules(modules, include_patterns, module_blacklist={'re'})
    assert len(list(objs)) == 1


def test_object_from_name():
    assert utils.object_from_name('pytest_wish.utils:object_from_name') == utils.object_from_name


def test_generate_objects_from_names():
    # normal path
    names = ['pytest_wish.utils:generate_objects_from_names']
    assert len(list(utils.generate_objects_from_names(names))) == 1
    # error paths
    names = ['# comment', 'non_existent_module:', 'math:non_existent_object']
    assert len(list(utils.generate_objects_from_names(names))) == 0

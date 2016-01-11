# -*- coding: utf-8 -*-

import re

import pkg_resources

from pytest_wish import utils


def test_import_coverage():
    """Fix the coverage by pytest-cov, that may trigger after pytest_wish is already imported."""
    from imp import reload  # Python 2 and 3 reload
    reload(utils)


def test_import_modules():
    assert len(utils.import_modules(['pytest_wish'])) == 1
    assert len(utils.import_modules(['pytest_wish'], module_blacklist={'pytest_wish'})) == 0


def test_import_distributions_modules():
    # normal code path, pytest is a dependency
    distributions = [pkg_resources.get_distribution('pytest-wish')]
    distributions_modules = utils.import_distributions_modules(distributions)
    assert len(distributions_modules) == 1
    requirement, distributions_modules = distributions_modules[0]
    assert requirement.startswith('pytest-wish==')
    assert set(distributions_modules) == {'pytest_wish', 'all'}

    # fail code path
    distributions_modules = utils.import_distributions_modules(
        distributions, distribution_blacklist={'pytest-wish'}
    )
    assert len(distributions_modules) == 0


def test_generate_module_objects():
    expected_item = ('generate_module_objects', utils.generate_module_objects)
    assert expected_item in list(utils.generate_module_objects(utils))


def test_valid_name():
    assert not utils.valid_name('math:factorial', [re.compile('a')], [])
    assert utils.valid_name('math:factorial', [re.compile('m')], [])
    assert utils.valid_name('math:factorial', [re.compile('.*factorial$')], [re.compile('moo')])
    assert not utils.valid_name('math:factorial', [re.compile('m')], [re.compile('math')])


def test_index_modules():
    assert utils.index_modules({'pytest_wish.utils': utils}, ['pytest_wish.utils:index'], [])


def test_generate_objects_from_names():
    # normal path
    names = ['pytest_wish.utils:generate_objects_from_names']
    assert len(list(utils.generate_objects_from_names(names))) == 1
    # error paths
    names = ['# comment', 'non_existent_module:', 'math:non_existent_object']
    assert len(list(utils.generate_objects_from_names(names))) == 0

# -*- coding: utf-8 -*-

import re

import pkg_resources

from pytest_wish import utils


def test_import_coverage():
    """Fix the coverage by pytest-cov, that may trigger after pytest_wish is already imported."""
    from imp import reload  # Python 2 and 3 reload
    reload(utils)


def test_import_modules():
    # normal code path, pytest is a dependency
    distributions = [pkg_resources.get_distribution('pytest')]
    distributions_modules = utils.import_modules(distributions)
    assert len(distributions_modules) == 1
    requirement, modules = distributions_modules[0]
    assert requirement.startswith('pytest==')
    assert set(modules) == {'_pytest', 'pytest'}

    # fail code path, pytest-wish is blacklisted
    distributions = [pkg_resources.get_distribution('pytest-wish')]
    distributions_modules = utils.import_modules(distributions)
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


def test_index_objects():
    # normal path
    assert utils.index_objects(['pytest_wish.utils:index_objects'])
    # error paths
    assert not utils.index_objects(['# comment', 'non_existent:', 'math:non_exixtent'])

# -*- coding: utf-8 -*-

import pkg_resources

import wish_utils


def test_import_modules():
    # normal code path, pytest is a dependency
    distributions = [pkg_resources.get_distribution('pytest')]
    distributions_modules = wish_utils.import_modules(distributions)
    assert len(distributions_modules) == 1
    requirement, modules = distributions_modules[0]
    assert requirement.startswith('pytest==')
    assert set(modules) == {'_pytest', 'pytest'}

    # fail code path, pytest-wish is blacklisted
    distributions = [pkg_resources.get_distribution('pytest-wish')]
    distributions_modules = wish_utils.import_modules(distributions)
    assert len(distributions_modules) == 0

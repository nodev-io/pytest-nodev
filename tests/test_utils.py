# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2016 Alessandro Amici
#

import re

from pytest_wish import utils


def test_import_coverage():
    """Fix the coverage by pytest-cov, that may trigger after pytest_wish is already imported."""
    from imp import reload  # Python 2 and 3 reload
    reload(utils)


def test_import_modules():
    assert len(utils.import_modules(['pytest_wish'])) == 1
    assert len(utils.import_modules(['pytest_wish'], module_blacklist=set())) == 1
    assert len(utils.import_modules(['pytest_wish'], module_blacklist={'pytest_wish'})) == 0
    assert len(utils.import_modules(['non_existent_module'])) == 0


def test_collect_distributions():
    assert len(list(utils.collect_distributions(['pytest-wish']))) == 1
    assert len(list(utils.collect_distributions(['non_existent_distribution']))) == 0
    assert len(list(utils.collect_distributions(['Python']))) == 1
    assert len(list(utils.collect_distributions(['all']))) > 1


def test_import_distributions():
    # normal code path, pytest is a dependency
    distributions_modules = utils.import_distributions(['pytest-wish'])
    assert len(distributions_modules) == 1
    requirement, distributions_modules = distributions_modules.popitem()
    assert requirement.startswith('pytest-wish==')
    assert set(distributions_modules) == {'pytest_wish'}

    distributions_modules = utils.import_distributions(['python'])
    assert len(distributions_modules) == 1
    requirement, distributions_modules = distributions_modules.popitem()
    assert requirement.startswith('Python==')
    assert 'os.path' in distributions_modules


def test_generate_module_objects():
    expected_item = ('generate_module_objects', utils.generate_module_objects)
    assert expected_item in list(utils.generate_module_objects(utils))


def test_valid_name():
    assert not utils.valid_name('math:factorial', [re.compile('a')], [])
    assert utils.valid_name('math:factorial', [re.compile('m')], [])
    assert utils.valid_name('math:factorial', [re.compile('.*factorial$')], [re.compile('moo')])
    assert not utils.valid_name('math:factorial', [re.compile('m')], [re.compile('math')])


def test_generate_objects_from_modules():
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

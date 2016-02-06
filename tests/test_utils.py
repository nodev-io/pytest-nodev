# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2016 Alessandro Amici
#

from pytest_wish import utils


def test_import_coverage():
    """Fix the coverage by pytest-cov, that may trigger after pytest_wish is already imported."""
    from imp import reload  # Python 2 and 3 reload
    reload(utils)


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

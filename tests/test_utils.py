# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2016 Alessandro Amici
#

import re

from pytest_nodev import utils


def test_import_coverage():
    """Fix the coverage by pytest-cov, that may trigger after pytest_nodev is already imported."""
    from imp import reload  # Python 2 and 3 reload
    reload(utils)


def test_extended_match():
    assert re.match(utils.exclude_include_pattern(), 'math:sin')

    assert re.match(utils.exclude_include_pattern('math'), 'math:sin')
    assert re.match(utils.exclude_include_pattern('.*:sin$'), 'math:sin')
    assert not re.match(utils.exclude_include_pattern('abc'), 'math:sin')

    assert not re.match(utils.exclude_include_pattern(exclude_pattern='math'), 'math:sin')
    assert not re.match(utils.exclude_include_pattern(exclude_pattern='.*:sin$'), 'math:sin')
    assert re.match(utils.exclude_include_pattern(exclude_pattern='abc'), 'math:sin')

    assert re.match(utils.exclude_include_pattern('m', exclude_pattern='moo'), 'math:sin')
    assert not re.match(utils.exclude_include_pattern('m', exclude_pattern='math'), 'math:sin')

# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2016 Alessandro Amici
#

from pytest_nodev import utils


def test_import_coverage():
    """Fix the coverage by pytest-cov, that may trigger after pytest_nodev is already imported."""
    from imp import reload  # Python 2 and 3 reload
    reload(utils)

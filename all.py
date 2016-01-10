# -*- coding: utf-8 -*-
"""If enabled in wish_utils this module imports all modules known to the packaging system."""

import pkg_resources

import pytest_wish.utils


if pytest_wish.utils.ENABLE_IMPORT_ALL:  # pragma: no branch
    pytest_wish.utils.import_distributions_modules(pkg_resources.working_set)

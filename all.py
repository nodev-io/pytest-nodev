# -*- coding: utf-8 -*-
"""If enabled in wish_utils this module imports all modules known to the packaging system."""

import pkg_resources

import wish_utils


if wish_utils.ENABLE_IMPORT_ALL:
    wish_utils.import_modules(pkg_resources.working_set)

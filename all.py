# -*- coding: utf-8 -*-
"""DANGER: this module will import all modules known to the packaging system as a side effect!"""

import pkg_resources

import wish_utils


wish_utils.import_modules(pkg_resources.working_set)

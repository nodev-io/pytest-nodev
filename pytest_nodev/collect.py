# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2016 Alessandro Amici
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

# python 2 support via python-future
from __future__ import absolute_import, unicode_literals
from builtins import str

import importlib
import inspect
import logging
import re
import sys

import pkg_resources
import stdlib_list

from . import blacklists
from . import utils


# regex representation of blacklists
MODULE_BLACKLIST_PATTERN = '|'.join(blacklists.MODULE_BLACKLIST) or utils.NOMATCH_PATTERN
OBJECT_BLACKLIST_PATTERN = '|'.join(blacklists.OBJECT_BLACKLIST) or utils.NOMATCH_PATTERN

logger = logging.getLogger('wish')


def collect_stdlib_distributions():
    # use Python long version number in distribution_spec
    distribution_spec = 'Python==%d.%d.%d' % sys.version_info[:3]
    # use Python short version number for stdlib_list as it supports only a few long versions
    distribution_module_names = stdlib_list.stdlib_list('%d.%d' % sys.version_info[:2])
    yield distribution_spec, distribution_module_names


def guess_module_names(distribution):
    if distribution.has_metadata('top_level.txt'):
        module_names = distribution.get_metadata('top_level.txt').splitlines()
    else:
        logger.info("Package %r has no top_level.txt. Guessing module name is %r.",
                    str(distribution.as_requirement()), distribution.project_name)
        module_names = [distribution.project_name]
    return module_names


def collect_installed_distributions():
    for distribution in pkg_resources.working_set:
        distribution_spec = str(distribution.as_requirement())
        distribution_module_names = guess_module_names(distribution)
        yield distribution_spec, distribution_module_names


def collect_distributions(specs):
    for spec in specs:
        try:
            distribution = pkg_resources.get_distribution(spec)
        except:
            logger.info("Failed to find a distribution matching the spec: %r.", spec)
            continue
        distribution_spec = str(distribution.as_requirement())
        distribution_module_names = guess_module_names(distribution)
        yield distribution_spec, distribution_module_names


def import_module(module_name, module_blacklist_pattern=MODULE_BLACKLIST_PATTERN):
    if re.match(module_blacklist_pattern, module_name):
        raise ImportError("Not importing blacklisted module: %r.", module_name)
    else:
        return importlib.import_module(module_name)


def import_distributions(distribution_modules, module_blacklist_pattern=MODULE_BLACKLIST_PATTERN):
    imported_module_names = []
    for spec, module_names in distribution_modules:
        for module_name in module_names:
            try:
                import_module(module_name, module_blacklist_pattern=module_blacklist_pattern)
                imported_module_names.append(module_name)
            except:
                logger.info("Failed to import module %r from package %r.", module_name, spec)
    return imported_module_names


def generate_module_objects(module, predicate=None):
    try:
        module_members = inspect.getmembers(module, predicate)
    except:
        logger.info("Failed to get member list from module %r.", module)
        raise StopIteration
    for object_name, object_ in module_members:
        if inspect.getmodule(object_) is module:
            yield object_name, object_


def generate_objects_from_modules(
        modules, include_patterns,
        exclude_patterns=[],
        predicate_name=None,
        module_blacklist_pattern=MODULE_BLACKLIST_PATTERN,
        object_blacklist_pattern=OBJECT_BLACKLIST_PATTERN,
):
    include_pattern = '|'.join(include_patterns) or utils.NOMATCH_PATTERN
    exclude_pattern = '|'.join(exclude_patterns) or utils.NOMATCH_PATTERN
    predicate = object_from_name(predicate_name) if predicate_name else None
    for module_name, module in modules.items():
        if re.match(module_blacklist_pattern, module_name):
            logger.debug("Not collecting objects from blacklisted module: %r.", module_name)
            continue
        for object_name, object_ in generate_module_objects(module, predicate):
            full_object_name = '{}:{}'.format(module_name, object_name)
            # NOTE: re auto-magically caches the compiled objects
            if re.match(include_pattern, full_object_name) \
                    and not re.match(exclude_pattern, full_object_name) \
                    and not re.match(object_blacklist_pattern, full_object_name):
                yield full_object_name, object_


def object_from_name(full_object_name):
    module_name, _, object_name = full_object_name.partition(':')
    module = importlib.import_module(module_name)
    return getattr(module, object_name)

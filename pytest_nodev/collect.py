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
"""
Helpers to import modules, collect modules top level objects and select/filter/blacklist them.
"""

# python 2 support via python-future
from __future__ import absolute_import, unicode_literals
from builtins import list, str

from distutils import sysconfig
import importlib
import inspect
import logging
import re
import pkgutil
import sys

import pkg_resources

from . import blacklists


# regex impossible to match (even in re.MULTILINE mode)
NOMATCH_PATTERN = r'.\A'

# regex representation of blacklists
MODULE_BLACKLIST_PATTERN = '|'.join(blacklists.MODULE_BLACKLIST) or NOMATCH_PATTERN
OBJECT_BLACKLIST_PATTERN = '|'.join(blacklists.OBJECT_BLACKLIST) or NOMATCH_PATTERN

logger = logging.getLogger('nodev')


def recurse_import_path(path=None, prefix='', spec='UNKOWN'):
    """Inspired to pkgutil.walk_packages with custom import logic and logging."""
    for _, name, ispkg in pkgutil.iter_modules(path, prefix):
        try:
            module = import_module(name)
        except BaseException as ex:  # catches Exception and SystemExit
            logger.info("Not imported sub-module %r from package %r: %s", name, spec, ex)
        else:
            if ispkg:
                recurse_import_path(path=module.__path__, prefix=name + '.', spec=spec)


def collect_stdlib_distributions():
    """Yield a conventional spec and the names of all top_level standard library modules."""
    distribution_spec = 'Python==%d.%d.%d' % sys.version_info[:3]
    stdlib_path = sysconfig.get_python_lib(standard_lib=True)
    distribution_top_level = [name for _, name, _ in pkgutil.iter_modules(path=[stdlib_path])]
    distribution_top_level += list(sys.builtin_module_names)
    yield distribution_spec, distribution_top_level


def guess_top_level(distribution):
    if distribution.has_metadata('top_level.txt'):
        module_names = distribution.get_metadata('top_level.txt').splitlines()
    else:
        logger.info("Package %r has no top_level.txt. Guessing module name is %r.",
                    str(distribution.as_requirement()), distribution.project_name)
        module_names = [distribution.project_name]
    return module_names


def collect_installed_distributions():
    """Yield the normalized spec and the names of top_level modules of all installed packages."""
    for distribution in pkg_resources.working_set:
        distribution_spec = str(distribution.as_requirement())
        distribution_top_level = guess_top_level(distribution)
        yield distribution_spec, distribution_top_level


def collect_distributions(specs):
    """Yield the normalized spec and the names of top_level modules of the requested specs."""
    for spec in specs:
        try:
            distribution = pkg_resources.get_distribution(spec)
        except Exception as ex:
            logger.info("Failed to find a distribution matching %r: %s", spec, ex)
            continue
        distribution_spec = str(distribution.as_requirement())
        distribution_top_level = guess_top_level(distribution)
        yield distribution_spec, distribution_top_level


def import_module(module_name, module_blacklist_pattern=MODULE_BLACKLIST_PATTERN):
    if re.match(module_blacklist_pattern, module_name):
        raise ImportError("module %r blacklisted." % module_name)
    else:
        return importlib.import_module(module_name)


def import_distributions(distribution_modules):
    top_level_modules = set()
    for spec, module_names in distribution_modules:
        for module_name in module_names:
            try:
                module = import_module(module_name)
            except BaseException as ex:  # catches Exception and SystemExit
                logger.info("Not imported top level %r from package %r: %s", module_name, spec, ex)
            else:
                path = getattr(module, '__path__', [])
                recurse_import_path(path=path, prefix=module_name + '.', spec=spec)
                # non-top_level module_names only add the first part, e.g. 'xml.dom' -> 'xml'
                top_level_modules.add(module_name.partition('.')[0])
    return top_level_modules


def generate_module_objects(module, predicate=None):
    try:
        module_members = inspect.getmembers(module, predicate)
    except Exception as ex:
        logger.info("Failed to get members of module %r: %s", module, ex)
        return
    for object_name, object_ in module_members:
        if inspect.getmodule(object_) is module:
            yield object_name, object_


def generate_objects_from_modules(
        modules, include_patterns,
        exclude_patterns=(),
        predicate_name=None,
        module_blacklist_pattern=MODULE_BLACKLIST_PATTERN,
        object_blacklist_pattern=OBJECT_BLACKLIST_PATTERN,
):
    include_pattern = '|'.join(include_patterns) or NOMATCH_PATTERN
    exclude_pattern = '|'.join(exclude_patterns) or NOMATCH_PATTERN
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
    """Return an object from its PEP3155 fully qualified name in the form "module:qualname".

    Inspired to how pkg_resources:EntryPoint.parse and pkg_resources:EntryPoint.load work."""
    module_name, _, object_name = full_object_name.partition(':')
    object_ = importlib.import_module(module_name)
    for attr_name in object_name.split('.'):
        object_ = getattr(object_, attr_name)
    return object_

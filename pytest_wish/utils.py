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

import collections
import importlib
import inspect
import logging
import re
import sys

import pkg_resources

import stdlib_list


# blacklists
MODULE_BLACKLIST = {
    # crash
    'icopen',
    'itertools',
    'ntpath',
    'test.support',
}
OBJECT_BLACKLIST = {
    # pytest internals
    '_pytest.runner:exit',
    '_pytest.runner:skip',
    '_pytest.skipping:xfail',

    # unconditional exit
    'faulthandler:_sigsegv',
    'posix:abort',
    'posix:_exit',
    'posix:fork',
    'posix:forkpty',
    'pty:fork',
    '_signal:default_int_handler',
    'atexit.register',

    # low level crashes
    'numpy.fft.fftpack_lite:cffti',
    'numpy.fft.fftpack_lite:rffti',
    'appnope._nope:beginActivityWithOptions',
    'ctypes:string_at',
    'ctypes:wstring_at',
    'gc:_dump_rpy_heap',
    'gc:dump_rpy_heap',
    'matplotlib._image:Image',
    'getpass:getpass',
    'getpass:unix_getpass',
    'ensurepip:_run_pip',

    # uninterruptable hang
    'itertools:cycle',
    'itertools:permutations',
    'itertools:repeat',

    # dangerous
    'os.mkdir',
    'pip.utils:rmtree',
}
EXCLUDE_PATTERNS = ['_|.*[.:]_']  # skip private modules and objects underscore-names

logger = logging.getLogger('wish')


def import_modules(module_names, requirement='', module_blacklist=MODULE_BLACKLIST):
    module_blacklist_pattern = '|'.join(module_blacklist)
    modules = collections.OrderedDict()
    for module_name in module_names:
        if module_blacklist_pattern and re.match(module_blacklist_pattern, module_name):
            logger.debug("Not importing blacklisted module: %r.", module_name)
        else:
            try:
                modules[module_name] = importlib.import_module(module_name)
            except:
                logger.info("Failed to import module %r (%r).", module_name, requirement)
    return modules


def collect_distributions(specs):
    distributions = collections.OrderedDict()
    for spec in specs:
        if spec.lower() in {'all', 'python'}:
            # fake distribution name for the python standard library
            distributions['Python==%d.%d.%d' % sys.version_info[:3]] = None
            if spec.lower() == 'all':
                # fake distribution name for all the modules known to the packaging system
                for distribution in pkg_resources.working_set:
                    distributions[str(distribution.as_requirement())] = distribution
        else:
            try:
                distribution = pkg_resources.get_distribution(spec)
                distributions[str(distribution.as_requirement())] = distribution
            except:
                logger.info("Failed to find a distribution matching the spec: %r.", spec)
    return distributions


def import_distributions(specs):
    distributions_modules = collections.OrderedDict()
    for requirement, distribution in collect_distributions(specs).items():
        if requirement.startswith('Python=='):
            python_version = requirement.partition('==')[2]
            # stdlib_list supports short versions and only a selected list of long versions
            python_short_version = python_version[:3]
            module_names = stdlib_list.stdlib_list(python_short_version)
        elif distribution.has_metadata('top_level.txt'):
            module_names = distribution.get_metadata('top_level.txt').splitlines()
        else:
            logger.info("Package %r has no top_level.txt. Guessing module name is %r.",
                        requirement, distribution.project_name)
            module_names = [distribution.project_name]
        modules = import_modules(module_names, requirement=requirement)
        distributions_modules[requirement] = list(modules.keys())
    return distributions_modules


def generate_module_objects(module, predicate=None):
    try:
        module_members = inspect.getmembers(module, predicate)
    except:
        logger.info("Failed to get member list from module %r.", module)
        raise StopIteration
    for object_name, object_ in module_members:
        if inspect.getmodule(object_) is module:
            yield object_name, object_


def valid_name(name, include_pattern, exclude_pattern):
    # NOTE: re auto-magically caches the compiled objects
    include_name = bool(include_pattern and re.match(include_pattern, name))
    exclude_name = bool(exclude_pattern and re.match(exclude_pattern, name))
    return include_name and not exclude_name


def generate_objects_from_modules(
        modules, include_patterns,
        exclude_patterns=EXCLUDE_PATTERNS,
        predicate_name=None,
        module_blacklist=MODULE_BLACKLIST,
        object_blacklist=OBJECT_BLACKLIST,
):
    exclude_patterns += tuple(name.strip() + '$' for name in object_blacklist)
    include_pattern = '|'.join(include_patterns)
    exclude_pattern = '|'.join(exclude_patterns)
    predicate = object_from_name(predicate_name) if predicate_name else None
    for module_name, module in modules.items():
        if module_name in module_blacklist:
            continue
        for object_name, object_ in generate_module_objects(module, predicate):
            full_object_name = '{}:{}'.format(module_name, object_name)
            if valid_name(full_object_name, include_pattern, exclude_pattern):
                yield full_object_name, object_


def object_from_name(full_object_name):
    module_name, _, object_name = full_object_name.partition(':')
    module = importlib.import_module(module_name)
    return getattr(module, object_name)


def generate_objects_from_names(stream):
    for line in stream:
        full_object_name = line.partition('#')[0].strip()
        if full_object_name:
            try:
                yield full_object_name, object_from_name(full_object_name)
            except ImportError:
                logger.info("Failed to import module for object %r.", full_object_name)
            except AttributeError:
                logger.info("Failed to import object %r.", full_object_name)

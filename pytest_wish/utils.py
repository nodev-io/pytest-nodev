# -*- coding: utf-8 -*-

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
DISTRIBUTION_BLACKLIST = set()
MODULE_BLACKLIST = {
    # crash
    'icopen',
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
    'posix:_exit',
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

    # dangerous
    'os.mkdir',
    'pip.utils:rmtree',
}
EXCLUDE_PATTERNS = [r'_', r'.*\._']

logger = logging.getLogger('wish')


def import_modules(module_names, requirement='', module_blacklist=MODULE_BLACKLIST):
    modules = collections.OrderedDict()
    for module_name in module_names:
        if module_name in module_blacklist:
            logger.debug("Not importing blacklisted module: %r.", module_name)
        else:
            try:
                modules[module_name] = importlib.import_module(module_name)
            except:
                logger.info("Failed to import module %r (%r).", module_name, requirement)
    return modules


def collect_distributions(distribution_names, distribution_blacklist=DISTRIBUTION_BLACKLIST):
    distributions = collections.OrderedDict()
    for distribution_name in distribution_names:
        if distribution_name in distribution_blacklist:
            logger.debug("Not importing blacklisted package: %r.", distribution_name)
        elif distribution_name.lower() in {'all', 'python'}:
            # fake distribution name for the python standard library
            distributions['Python==%d.%d.%d' % sys.version_info[:3]] = None
            if distribution_name.lower() == 'all':
                # fake distribution name for all the modules known to the packaging system
                for distribution in pkg_resources.working_set:
                    distributions[str(distribution.as_requirement())] = distribution
        else:
            try:
                distribution = pkg_resources.get_distribution(distribution_name)
                distributions[str(distribution.as_requirement())] = distribution
            except:
                logger.info("Failed to find package %r.", distribution_name)
    return distributions


def import_distributions(distribution_names, distribution_blacklist=DISTRIBUTION_BLACKLIST):
    distributions_modules = collections.OrderedDict()
    distributions = collect_distributions(distribution_names, distribution_blacklist)
    for requirement, distribution in distributions.items():
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


def valid_name(name, include_res, exclude_res):
    include_name = any(include_re.match(name) for include_re in include_res)
    exclude_name = any(exclude_re.match(name) for exclude_re in exclude_res)
    return include_name and not exclude_name


def generate_objects_from_modules(
        modules, include_patterns,
        exclude_patterns=EXCLUDE_PATTERNS,
        predicate_name=None,
        module_blacklist=MODULE_BLACKLIST,
        object_blacklist=OBJECT_BLACKLIST,
):
    exclude_patterns += tuple(name.strip() + '$' for name in object_blacklist)
    include_res = [re.compile(pattern) for pattern in include_patterns]
    exclude_res = [re.compile(pattern) for pattern in exclude_patterns]
    predicate = object_from_name(predicate_name) if predicate_name else None
    for module_name, module in modules.items():
        if module_name in module_blacklist:
            continue
        for object_name, object_ in generate_module_objects(module, predicate):
            full_object_name = '{}:{}'.format(module_name, object_name)
            if valid_name(full_object_name, include_res, exclude_res):
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

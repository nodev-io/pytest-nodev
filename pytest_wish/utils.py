
import importlib
import inspect
import logging
import re


# if set to True 'import all' imports all modules known to the packaging system.
ENABLE_IMPORT_ALL = False

# blacklists
DISTRIBUTION_BLACKLIST = set()
MODULE_BLACKLIST = set()
OBJECT_BLACKLIST = {
    # pytest internals
    '_pytest.runner:exit',
    '_pytest.runner:skip',
    '_pytest.skipping:xfail',

    # unconditional exit
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

    # hangs
    'Tkinter:mainloop',
    'astkit.compat.py3:execfile',
    'astroid.builder:open_source_file',
    'click.termui:getchar',
    'click.termui:edit',
    'click.termui:hidden_prompt_func',
    'click.termui:launch',
    'eventlet.hubs:trampoline',
    'getpass:getpass',
    'getpass:unix_getpass',
    'itertools:cycle',
    'matplotlib.font_manager:FontManager',
    'networkx.tests.test:run',
    'nose.plugins.plugintest:run',
    'numpy:nditer',
    'pty:_copy',
    'pydoc:serve',
    'pyexpat:ErrorString',
    'skimage:_test',
    'skimage:test',
    'webbrowser:open',

    # dangerous
    'os.mkdir',
    'pip.utils:rmtree',
}
EXCLUDE_PATTERNS = [r'_', r'.*\._']

logger = logging.getLogger('wish')


def import_modules(module_names, module_blacklist=MODULE_BLACKLIST):
    return [importlib.import_module(name) for name in module_names if name not in module_blacklist]


def import_distributions_modules(distributions, distribution_blacklist=DISTRIBUTION_BLACKLIST):
    distributions_modules = []
    for distribution in distributions:
        requirement = str(distribution.as_requirement())
        if distribution.project_name in distribution_blacklist:
            logger.debug("Not importing blacklisted package: %r.", requirement)
            continue
        if distribution.has_metadata('top_level.txt'):
            module_names = distribution.get_metadata('top_level.txt').splitlines()
        else:
            logger.info("Package %r has no top_level.txt. Assuming module name is %r.",
                        requirement, distribution.project_name)
            module_names = [distribution.project_name]
        for module_name in module_names:
            try:
                importlib.import_module(module_name)
            except:
                logger.info("Failed to import module %r (%r).", module_name, requirement)
        distributions_modules.append((requirement, module_names))
    return distributions_modules


def generate_module_objects(module):
    try:
        module_members = inspect.getmembers(module)
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
        object_blacklist=OBJECT_BLACKLIST
):
    exclude_patterns += tuple(name.strip() + '$' for name in object_blacklist)
    include_res = [re.compile(pattern) for pattern in include_patterns]
    exclude_res = [re.compile(pattern) for pattern in exclude_patterns]
    for module_name, module in modules.items():
        for object_name, object_ in generate_module_objects(module):
            full_object_name = '{}:{}'.format(module_name, object_name)
            if valid_name(full_object_name, include_res, exclude_res):
                yield full_object_name, object_


def generate_objects_from_names(stream):
    module_index = {}
    for line in stream:
        full_object_name = line.partition('#')[0].strip()
        if full_object_name:
            module_name, _, object_name = full_object_name.partition(':')
            try:
                module = module_index.setdefault(module_name, importlib.import_module(module_name))
                yield full_object_name, getattr(module, object_name)
            except ImportError:
                logger.info("Failed to import module %r.", module_name)
            except AttributeError:
                logger.info("Failed to import object %r.", full_object_name)

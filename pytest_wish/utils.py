
import importlib
import inspect
import re


# if set to True 'import all' imports all modules known to the packaging system.
ENABLE_IMPORT_ALL = False

# blacklists
DISTRIBUTION_BLACKLIST = {
    'pytest-wish',
}
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
    'eventlet.hubs:trampoline',
    'getpass:getpass',
    'getpass:unix_getpass',
    'matplotlib.font_manager:FontManager',
    'pty:_copy',
    'pydoc:serve',
    'pyexpat:ErrorString',
    'skimage:_test',
    'skimage:test',
}


def import_modules(distributions):
    distribution_modules = []
    for distribution in distributions:
        if distribution.project_name in DISTRIBUTION_BLACKLIST:
            continue
        if not distribution.has_metadata('top_level.txt'):
            continue
        module_names = distribution.get_metadata('top_level.txt').splitlines()
        for module_name in module_names:
            try:
                importlib.import_module(module_name)
            except:  # pragma: no cover
                pass
        distribution_requirement = str(distribution.as_requirement())
        distribution_modules.append((distribution_requirement, module_names))
    return distribution_modules


def generate_module_objects(module):
    try:
        module_members = inspect.getmembers(module)
    except:  # pragma: no cover
        raise StopIteration
    for object_name, object_ in module_members:
        if inspect.getmodule(object_) is module:
            yield object_name, object_


def valid_name(name, include_res, exclude_res):
    include_name = any(include_re.match(name) for include_re in include_res)
    exclude_name = any(exclude_re.match(name) for exclude_re in exclude_res)
    return include_name and not exclude_name


def index_modules(modules, include_patterns, exclude_patterns, object_blacklist=OBJECT_BLACKLIST):
    exclude_patterns += tuple(name.strip() + '$' for name in object_blacklist)
    include_res = [re.compile(pattern) for pattern in include_patterns]
    exclude_res = [re.compile(pattern) for pattern in exclude_patterns]
    object_index = {}
    for module_name, module in modules.items():
        for object_name, object_ in generate_module_objects(module):
            full_object_name = '{}:{}'.format(module_name, object_name)
            if valid_name(full_object_name, include_res, exclude_res):
                object_index[full_object_name] = object_
    return object_index


def index_objects(stream):
    module_index = {}
    object_index = {}
    for line in stream:
        full_object_name = line.partition('#')[0].strip()
        if full_object_name:
            module_name, _, object_name = full_object_name.partition(':')
            try:
                module = module_index.setdefault(module_name, importlib.import_module(module_name))
                object_index[full_object_name] = getattr(module, object_name)
            except ImportError:
                pass
            except AttributeError:
                pass
    return object_index

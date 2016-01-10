
import importlib

DISTRIBUTION_BLACKLIST = {
    'pytest-wish',
}

# if set to True 'import all' imports all modules known to the packaging system.
ENABLE_IMPORT_ALL = False


def import_modules(distributions):
    distribution_modules = []
    for distribution in distributions:
        if distribution.project_name in DISTRIBUTION_BLACKLIST:
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

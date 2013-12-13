"""
This module provide helper function to deal with orchester modules
You should use the provided helper functions instead to interact with
plugin modules.

"""

ORCHESTER_MODULE_PATH = 'orchester.plugins'

def get_plugin_class(name):
    """
    Returns the class of an orchester plugin by its name.
    Returns None if not found.

    This helper function works with all plugin types.

    """
    import importlib

    mod_name = "%s.%s" % (ORCHESTER_MODULE_PATH, name)
    try:
        mod = importlib.import_module(mod_name)
    except:
        print "Cannot import %s" % mod_name
        return None
    return mod.get_class()


def get_plugin_instance(name, *args, **kwargs):
    """
    Same as get_plugin_class but returns an actual instance of the
    plugin instead of his class.

    *args and **kwargs are passed to the instance __init__ method.

    """
    klass = get_plugin_class(name)
    if klass:
        return klass(*args, **kwargs)
    else:
        return None


def get_plugin_version(name):
    """
    This method returns the version of the plugin _name_ by calling its
    smethod get_version().

    Returns 0 if the plugin or the version is not found.

    """
    klass = get_plugin_class(name)
    if klass:
        return klass.get_version()
    else:
        return 0
 

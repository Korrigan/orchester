"""
This module defines the base classes for orchester plugin implementations
This acts as a reference for every plugin implemented

"""

class AbstractBasePlugin(object):
    """
    This is an abstract for plugin management.
    All plugins should inherits from this class or a child class.


    """

    @classmethod
    def get_name(kls):
        """
        This method returns the plugin name.

        Child class must either override this method or define a name
        attribute.

        """
        if kls.name:
            return kls.name
        return ""

    @classmethod
    def get_version(kls):
        """
        This method returns the plugin version.

        Child class must either override this method or define a
        _version attribute.

        """
        if kls.version:
            return kls.version
        return 0


def get_class():
    """
    This is a helper function to get the plugin class from the plugin
    name.

    Every plugin module must implement this function.

    """
    return AbstractBasePlugin

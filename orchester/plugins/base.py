"""
This module defines the base classes for orchester plugin implementations
This acts as a reference for every plugin implementation

"""


class AbstractBasePlugin(object):
    """
    This is an abstract for plugin management.
    All plugins should inherits from this class or a child class.


    """
    def __init__(self, *args, **kwargs):
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

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

    @classmethod
    def get_extra_kwargs(kls, app):
        """
        This method returns the extra configuration kwargs needed to be sent to
        the node for worker deployment.

        It takes information from app wich is an instance of
        orchester.models.application.Application

        By default returns an empty dict, an useful implementation should returns a dict

        Child class must implement all their required argument here

        Node daemon will instanciate the plugin with these keywords
        arguments if provided

        """
        return {}


def get_class():
    """
    This is a helper function to get the plugin class from the plugin
    name.

    Every plugin module must implement this function.

    """
    return AbstractBasePlugin

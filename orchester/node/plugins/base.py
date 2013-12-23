"""
This module implements base plugins for orchester-node

"""

from orchester.plugins import get_plugin_class


class WorkerAbstractBasePlugin(get_plugin_class('base')):
    """
    This class is the base class for worker node plugins
    Every node plugins should inherits of this class

    """

    @classmethod
    def get_extra_kwargs(kls, app):
        """
        This method returns the extra configuration kwargs needed to be sent to
        the node for worker deployment.

        It takes information from app wich is an instance of
        orchester.models.application.Application

        By default returns None, an useful implementation must returns a dict

        Child class must implement all their required argument here

        Node daemon will instanciate the plugin with these keywords
        arguments if provided

        """
        return None


def get_class():
    """Returns the WorkerAbstractBasePlugin class"""
    return WorkerAbstractBasePlugin

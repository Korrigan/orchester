"""
This module is a dummy plugin for orchester

"""

from orchester.plugins.base import AbstractBasePlugin

class DummyPlugin(AbstractBasePlugin):
    """
    This is a dummy plugin to show orchester plugin implementation

    """
    name = 'dummy'
    version = 42


def get_class():
    """Helper function to get the plugin class"""
    return DummyPlugin

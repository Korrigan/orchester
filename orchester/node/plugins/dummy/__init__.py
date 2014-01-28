"""
Dummy node plugin for testing purposes
Basically does nothing

"""

from orchester.plugin.dummy import DummyPlugin

def get_class():
    """
    This method returns the orchester generic dummy plugin class

    """
    return DummyPlugin

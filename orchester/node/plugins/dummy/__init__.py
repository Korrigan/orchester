"""
Dummy node plugin for testing purposes
Basically does nothing

"""

from orchester.plugins.dummy import DummyPlugin

def get_class():
    """
    This method returns the orchester generic dummy plugin class

    """
    return DummyPlugin

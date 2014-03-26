"""
Utility functions and stuff useful for each component

"""

from fabric.api import *

from . import defaults
from .releases import ReleaseManager

def load_environ_settings(settings, environ):
    """
    Load settings[environ] into the fabric env

    The settings dictionary is particular:
     - the key "defaults" is reserved and will be loaded before
       settings[environ]
     - if settings[environ] is a string, settings will be loaded from
       settings[settings[environ]] instead (recursively)

    This function will first load default.settings. It will also set the environ
    setting and the git_branch setting. This is, however, done at the very
    beginning so it can be overrided

    Finally, if release_path is set, this function with instanciate a
    ReleaseManager into env.releases

    """
    defaults.check_environ(environ, settings)
    if not isinstance(settings[environ], dict):
        return load_environ_settings(settings, settings[environ])
    env.update(defaults.settings)
    env.environ = environ
    env.git_branch = defaults.git_branch[environ]
    if settings.has_key('default'):
        env.update(settings['default'])
    env.update(settings[environ])
    if env.has_key('release_path'):
        env.releases = ReleaseManager(env.release_path)

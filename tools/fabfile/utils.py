"""
Utility functions and stuff useful for each component

"""

import os

from fabric.api import *
from fabric.colors import blue
import fabtools

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


def setup():
    """
    Setup the virtualenv and the directory structures

    """
    print blue("Creating virtualenv in %s" % env.virtualenv)
    run("virtualenv --clear %s" % env.virtualenv)
    print blue("Making directories")
    fabtools.require.files.directory(env.app_path)
    fabtools.require.files.directory(env.release_path)


def create_release():
    """
    Creates and return a new release

    """
    print blue("Cloning repository %s [branch %s]" % (env.repository, env.git_branch))
    return env.releases.create()

def commit_release():
    """
    Commits to the latest release

    """
    print blue("Deploying new release")
    env.releases.commit()

def list_releases():
    """
    Lists all the releases and who deployed it

    """
    import StringIO
    import json

    print blue("Releases list")
    for r in env.releases.list():
        mdata = {
            'user': '<somebody>',
            'host': '<somewhere>',
            'environ': '<some_env>'
        }
        path = os.path.join(env.release_path, r, 'deploy.json')
        raw = StringIO.StringIO()
        with quiet():
            if get(path, raw).succeeded:
                mdata = json.loads(raw.getvalue())
                raw.close()
            print " - %(release)s: deployed by %(user)s@%(host)s" % {
                'release': r,
                'user': mdata['user'],
                'host': mdata['host'],
            }

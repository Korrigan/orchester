"""
Fabric module to interact with orchester.master component

"""
import os

from fabric.api import *
from fabric.colors import blue
import fabtools

from . import defaults
from . import utils 


project = 'orchester-master'
app_path = os.path.join(defaults.base_app_dir, project)

settings = {
    'default': {
        'virtualenv': os.path.join(defaults.base_venv_dir, project),
        'app_path': app_path,
        'release_path': os.path.join(app_path, 'release'),
        'current_path': os.path.join(app_path, 'current'),
    },
    'staging': {},
    'prod': 'staging',
}


@task
def setup(environ=defaults.environ):
    """
    Setup the directory structure for orchester-master component

    """
    defaults.check_environ(environ)
    utils.load_environ_settings(settings, environ)
    utils.setup()


@task
def deploy(environ=defaults.environ):
    """
    Deploys the master with the specified environment

    """
    defaults.check_environ(environ)
    utils.load_environ_settings(settings, environ)
    utils.create_release()
    utils.commit_release()
    print blue("Restarting services")


@task
def releases(environ=defaults.environ):
    defaults.check_environ(environ)
    utils.load_environ_settings(settings, environ)
    utils.list_releases()


@task
def rollback(environ=defaults.environ,release=None):
    """
    Rollback to release or the previous release

    """
    defaults.check_environ(environ)
    utils.load_environ_settings(settings, environ)
    if release:
        env.releases.set_current(release)
    else:
        env.releases.rollback()

"""
Fabric module to interact with orchester.node component

"""
import os

from fabric.api import *

from . import defaults
from . import utils

project = 'orchester-node'
app_path = os.path.join(defaults.base_app_dir, project)
shared_path = os.path.join(app_path, 'shared')
current_path = os.path.join(app_path, 'current')

settings = {
    'default': {
        'project': project,
        'virtualenv': os.path.join(defaults.base_venv_dir, project),
        'app_path': app_path,
        'release_path': os.path.join(app_path, 'release'),
        'current_path': current_path,
        'etc_path': os.path.join(current_path, 'etc', project),
        'shared_path': shared_path,
        'log_path': os.path.join(shared_path, 'log'),
        'tests_package': 'orchester.tests.node',
        'pid_file': os.path.join(shared_path, project + ".pid"),
        'gunicorn_app': 'orchester.node:setup()'
    },
    'staging': {},
    'prod': 'staging',
}


@task
def setup(environ=defaults.environ):
    """
    Setup the directory structure for orchester-node component

    """
    defaults.check_environ(environ)
    utils.load_environ_settings(settings, environ)
    utils.setup()


@task
def deploy(environ=defaults.environ):
    """
    Deploys the node with the specified environment

    """
    defaults.check_environ(environ)
    utils.load_environ_settings(settings, environ)
    utils.create_release()
    utils.install_requirements()
    utils.run_tests()
    utils.update_configuration()
    utils.commit_release()
    utils.restart_services()


@task
def releases(environ=defaults.environ):
    """
    Lists releases and their metadata

    """
    defaults.check_environ(environ)
    utils.load_environ_settings(settings, environ)
    utils.list_releases()

@task
def rollback(release=None):
    """
    Rollback to `release` or the previous release if release is None

    """
    defaults.check_environ(defaults.environ)
    utils.load_environ_settings(settings, defaults.environ)
    utils.rollback_release(release)
    utils.restart_services()

"""
Fabric module to interact with orchester.master component

"""
import os

from fabric.api import *
from fabric.colors import blue
import fabtools

from . import defaults
from .utils import load_environ_settings


project = 'orchester-master'
app_path = os.path.join(defaults.base_app_dir, project)
master_hosts = ['212.83.161.166']

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
@hosts(master_hosts)
def setup(environ=defaults.environ):
    """
    Setup the directory structure for orchester-master component

    """
    defaults.check_environ(environ)
    load_environ_settings(settings, environ)
    print blue("Creating virtualenv in %s" % env.virtualenv)
    run("virtualenv --clear %s" % env.virtualenv)
    print blue("Making directories")
    fabtools.require.files.directory(env.app_path)
    fabtools.require.files.directory(env.release_path)


@task
@hosts(master_hosts)
def deploy(environ=defaults.environ):
    """
    Deploys the master with the specified environment

    """
    defaults.check_environ(environ)
    load_environ_settings(settings, environ)
    print blue("Cloning repository %s [branch %s]" % (env.repository, env.git_branch))
    release = env.releases.create()
    print blue("Deploying new release '%s'" % release)
    env.releases.commit()
    print blue("Restarting services")

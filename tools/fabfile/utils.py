"""
Utility functions and stuff useful for each component

"""

import os
import StringIO
import json

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
    Also generate the gunicorn configuration used by supervisor

    """
    print blue("Creating virtualenv in %s" % env.virtualenv)
    run("virtualenv --clear %s" % env.virtualenv)
    print blue("Making directories")
    fabtools.require.files.directory(env.app_path)
    fabtools.require.files.directory(env.release_path)
    fabtools.require.files.directory(env.shared_path)
    fabtools.require.files.directory(env.log_path)


def create_release():
    """
    Creates and return a new release

    """
    print blue("Cloning repository %s [branch %s]" % (env.repository, env.git_branch))
    release = env.releases.create()
    env.new_release_path = os.path.join(env.release_path, str(release))
    return release


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


def install_requirements():
    """
    Installs required python packages with pip in the virtualenv

    """
    print blue("Installing requirements")
    with fabtools.python.virtualenv(env.virtualenv):
        run("pip install -r %s" % os.path.join(env.new_release_path, 'requirements.txt'))


def generate_config_file(tpl_path, dst_path, tpl_context=None, check_config=None):
    """
    Generates a config file by using template `tpl_path` and `context` and put
    it under `path`

    If `check_config` is a callable, this function will call it to check the
    configuration

    """
    contents = StringIO.StringIO()
    if get(tpl_path, contents).failed:
        abort("Cannot open %s" % tpl_path)
    fabtools.require.files.template_file(path=dst_path,
                                         template_contents=contents.getvalue(),
                                         context=tpl_context)
    contents.close()
    if callable(check_config):
        check_config()


def update_gunicorn_configuration(base_path):
    """
    Updates and check the gunicorn config

    """
    gunicorn_tpl_fp = os.path.join(base_path, 'gunicorn.%s.conf' % env.environ)
    gunicorn_conf_fp = os.path.join(base_path, 'gunicorn.conf')
    gunicorn_context = {
        'app_path': env.current_path,
        'access_log': os.path.join(env.log_path, 'access.log'),
        'error_log': os.path.join(env.log_path, 'errror.log'),
        'pid_file': env.pid_file,
    }
    def _check():
        with path(os.path.join(env.virtualenv, 'bin'), behavior='replace'):
            with cd(env.new_release_path):
                run('gunicorn --check-config -c %s "%s"' % (gunicorn_conf_fp, env.gunicorn_app))
    generate_config_file(gunicorn_tpl_fp, gunicorn_conf_fp, gunicorn_context, _check)


def update_supervisor_configuration(base_path):
    """
    Updates supervisor config

    """
    supervisor_tpl_fp = os.path.join(base_path, 'supervisor.%s.conf' % env.environ)
    supervisor_conf_fp = os.path.join(base_path, 'supervisor.conf')
    supervisor_context = {
        'gunicorn_conf': os.path.join(base_path, 'gunicorn.conf'),
        'virtualenv': env.virtualenv,
        'user': env.user,
        'log_file': os.path.join(env.log_path, 'supervisor.log'),
        'gunicorn_app': env.gunicorn_app,
    }
    generate_config_file(supervisor_tpl_fp, supervisor_conf_fp, supervisor_context)


def update_configuration():
    """
    Regenerate gunicorn configuration from the template

    """
    print blue("Updating configuration")
    new_etc_path = env.etc_path.replace(env.current_path, env.new_release_path)
    update_gunicorn_configuration(new_etc_path)
    update_supervisor_configuration(new_etc_path)

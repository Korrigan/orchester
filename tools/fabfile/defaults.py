"""
This module defines the global defaults for all tasks

"""

# Environment
user = "orchester"
environ = "staging"
available_environs = ["staging", "prod"]

# Git
git_repo = "https://github.com/Korrigan/orchester.git"
git_branch = {
    'staging': 'master',
    'prod': 'master',
}

# Paths
base_dir = "/home/orchester"
base_venv_dir = "/home/orchester/.virtualenv"
base_app_dir = "/home/orchester/orchester.io"

# Settings
settings = {
    'user': user,
    'base_dir': base_dir,
    'base_app_dir': base_app_dir,
    'repository': git_repo,
}

def check_environ(environ, env_list=available_environs):
    """
    Check if environ is valid and abort if not

    """
    from fabric.api import abort

    if not environ in env_list:
        abort("No environment named '%s' available" % environ)
    return True

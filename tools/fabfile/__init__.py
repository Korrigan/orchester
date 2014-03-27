"""
Main fabfile for orchester.io project

- Roles and stuff are defined in .staging and .prod modules
- Commands and workflow for master are defined in .master module
- Commands and workflow for node are defined in .node module

Global fabfile usage is `fab <component>.<command>:<env>` with
 - <component>: master or node
 - <command>: See submodules for further info
 - <env>: staging or prod (staging by default)

Please note that for the node, you have to specify one or more hosts on the
command line with the -H flag.

"""
from fabric.api import *

from . import defaults
from . import master
from . import node

@task
def defaults():
    """
    This task prints out the defaults configuration variables defined in this
    fabric module

    """
    print "Environment: %s" % defaults.environ
    print "Git branch: %s" % defaults.git_branch[defaults.environ]

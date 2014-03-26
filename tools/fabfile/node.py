"""
Fabric module to interact with orchester.node component

"""
from fabric.api import *

from . import defaults

@task
def deploy(environ=defaults.environ):
    """
    Deploys a node with the specified environment

    """
    defaults.check_environ(environ)
    print "Deploying orchester.node [%s] on %s" % (environ, env.host)

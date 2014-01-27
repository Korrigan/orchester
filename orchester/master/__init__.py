"""
This module is the entry point of the orchester-master daemon

"""

from flask import Flask
from flask.ext.mongoengine import MongoEngine


app = Flask('orchester.master')
db = MongoEngine()


def setup(db_name='orchester'):
    """
    This function configures database and register urls

    """
    from .api import register

    app.config['MONGODB_SETTINGS'] = {
        'DB': db_name,
    }
    db.init_app(app)
    register(app)


class Master(object):
    """
    This class is the main class of orchester-master.
    It deals with all scaling and worker repartition features

    """

    def get_node(self):
        """
        Returns a host object depending of load metrics

        """
        return Node.objects.first()

    def deploy(self, app):
        """
        Deploy an application to one or more nodes

        """
        for i in range(0, app.min_workers):
            node = self.get_node()
            if not node:
                print "No node available for deployment"
                # throw smth
            node.deploy(app)

master = Master()

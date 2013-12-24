"""
This module is the entry point of the orchester-master daemon

"""

from flask import Flask
from flask.ext.mongoengine import MongoEngine

from .api import register


app = Flask('orchester.master')
app.config['MONGODB_SETTINGS'] = {
    'DB': 'orchester',
    }
db = MongoEngine(app)

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
                pass #throw smth
            node.deploy(app)

master = Master()

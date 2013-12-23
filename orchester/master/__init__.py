"""
This module is the entry point of the orchester-master daemon

"""

from flask import Flask
from flask.ext.mongoengine import MongoEngine

from .api import index


app = Flask('orchester.master')
app.config['MONGODB_SETTINGS'] = {
    'DB': 'orchester',
    }
db = MongoEngine(app)
app.register_blueprint(index)

class Master(object):
    """
    This class is the main class of orchester-master.
    It deals with all scaling and worker repartition features

    """

    def get_node(self):
        """
        Returns a host object depending of load metrics

        """
        pass

    def deploy(self, app):
        """
        Deploy an application to one or more nodes

        """
        for i in range(0, app.min_workers):
            node = self.get_node()
            node.deploy(app)

master = Master()

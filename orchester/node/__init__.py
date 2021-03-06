"""
This module is the entry point of the orchester-node daemon

"""

from flask import Flask

from .api import index
from .api.worker import worker
from .api.monitoring import monitoring


app = Flask('orchester.node')

class Node(object):
    """
    Node class manages the current workers

    """
    workers = []

    def __init__(self, *args, **kwargs):
        import socket
        self.hostname = socket.gethostname()

    def get_metrics(self):
        """Returns metrics collected from .monitoring.get_global_metrics()"""
        from .monitoring import get_global_metrics
        return get_global_metrics()

node = Node()

def setup():
    app.register_blueprint(index)
    app.register_blueprint(worker, url_prefix='/worker')
    app.register_blueprint(monitoring, url_prefix='/monitoring')
    return app

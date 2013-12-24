"""
This module is the entry point of the orchester-node daemon

"""

from flask import Flask

from .api import index
from .api.worker import worker


app = Flask('orchester.node')
app.register_blueprint(index)
app.register_blueprint(worker, url_prefix='/worker')

class Node(object):
    """
    Node class manages the current workers

    """
    workers = []

    def __init__(self, *args, **kwargs):
        import socket
        self.hostname = socket.gethostname()

node = Node()

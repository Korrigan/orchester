"""
This module is the entry point of the orchester-node daemon

"""

from flask import Flask

from .api import index


app = Flask('orchester.node')
app.register_blueprint(index)

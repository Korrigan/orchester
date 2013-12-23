"""
This module is the entry point of the orchester-master daemon

"""

from flask import Flask

from .api import index


app = Flask('orchester.master')
app.register_blueprint(index)

"""
This module contains client API views

"""

from .application import application

def register(app):
    """Register client API urls"""
    app.register_blueprint(application, url_prefix='/app')

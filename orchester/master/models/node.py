"""
This module handles node related models

"""

from orchester.plugins import get_node_plugin_class
from orchester.master import db

from . import DisplayableModelMixin


class Node(db.Document, DisplayableModelMixin):
    """
    This class represents a node instance

    """
    host = db.StringField()

    def deploy(self, app):
        """
        This method deploys the instance of Application to the node

        """
        from flask import json
        from .worker import Worker

        plugin = 'dummy' # We should have a way to add a plugin selector
        klass = get_node_plugin_class(plugin)
        if not klass:
            raise "toto"
        data = {
            'plugin_name': plugin,
            'private_key': app.private_key,
            'code_url': app.code_url,
            'env_vars': app.env_vars,
            'extra': klass.get_extra_kwargs(app)
            }
        if app.code_tag:
            data['code_tag'] = app.code_tag 
        ret = '{ "id": "tachatte" }' # From node API call
        ret_data = json.loads(ret)
        wkr = Worker(host=self, worker_id=ret_data['id'], app=app)
        wkr.save()

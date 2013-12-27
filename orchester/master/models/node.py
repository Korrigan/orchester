"""
This module handles node related models

"""

from orchester.plugins import get_node_plugin_class
from orchester.master import db


class Node(db.Document):
    """
    This class represents a node instance

    """
    host = db.StringField()

    def deploy(self, app):
        """
        This method deploys the instance of Application to the node

        """
        plugin = 'docker'
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
        ret = "" # From node API call
        ret_data = json.decode(ret)
        app.workers.push(Worker(host=self, worker_id=ret_data['id']))


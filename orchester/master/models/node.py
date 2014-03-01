"""
This module handles node related models

"""

import requests
from flask import json

from orchester.plugins import get_node_plugin_class
from orchester.master import db

from . import DisplayableModelMixin


class Node(db.Document, DisplayableModelMixin):
    """
    This class represents a node instance

    """
    host = db.StringField()

    @property
    def url(self):
        """Returns the host http(s) url"""
        return "http://" + self.host

    def delete(self, *args, **kwargs):
        """
        Deletes all the workers on the node and then deletes the node
        """
        from .worker import Worker

        Worker.bulk_delete(host=self)
        return super(Node, self).delete(*args, **kwargs)

    def deploy(self, app):
        """
        This method deploys the instance of Application to the node

        """
        from .worker import Worker

        plugin = 'dummy' # We should have a way to add a plugin selector
        klass = get_node_plugin_class(plugin)
        if not klass:
            raise "toto" # To fix
        data = {
            'plugin_name': plugin,
            'private_key': app.private_key,
            'code_url': app.code_url,
            'code_type': app.code_type,
            'env_vars': app.env_vars,
            'extra': klass.get_extra_kwargs(app)
        }
        if app.code_tag:
            data['code_tag'] = app.code_tag 
        ret = requests.post(self.url + '/worker/', data=json.dumps(data))
        if not ret.status_code == 200: # Should be 201
            print "Bad status code of %d" % ret.status_code
        ret_data = ret.json()
        wkr = Worker(host=self, worker_id=ret_data['id'], app=app)
        wkr.save()

    def stop_worker(self, worker):
        """
        This method deletes a worker from a node

        """
        ret = requests.delete(self.url + '/worker/' + worker.worker_id)
        if not ret.status_code == 200:
            print "Deletion failed: %s" ret.text

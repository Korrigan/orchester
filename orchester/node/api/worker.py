from flask import Blueprint, request, jsonify
from flask.views import MethodView

from orchester.api import views


worker = Blueprint('worker', __name__)

def worker_jsonify(worker):
    """
    Helper method to dump content of a worker

    """
    data = {
        'id': worker.id,
        'plugin_name': worker.plugin.name,
        'plugin_version': worker.plugin.version,
    }
    return jsonify(data)

@worker.route('/<id>')
def worker_get(id):
    """
    Dump the specified worker

    """
    from werkzeug.exceptions import abort
    from orchester.node import node
    for worker in node.workers:
        if worker.id == id:
            return worker_jsonify(worker)
    abort(404)

class WorkerView(MethodView):
    methods = ['GET', 'POST']

    def get(self):
        """
        Get method return the list of workers on the node

        """
        from orchester.node import node
        data = {
            'workers': [],
        }
        for worker in node.workers:
            data['workers'].append('https://%s.orchester.io/api/.../worker/%s' % (node.hostname, worker.id))
        data['count'] = len(data['workers'])
        return jsonify(data)
        
    def post(self):
        """
        Post method return a new worker if data sent is validated

        """
        from orchester.node.worker import Worker
        from orchester.plugins import get_node_plugin_instance
        from werkzeug.exceptions import abort
        from orchester.node import node
        from flask import json
        data = json.loads(request.data)
        if not 'plugin_name' in data:
            abort(400)
        plugin = get_node_plugin_instance(data['plugin_name'], **data.get('extra', {}))
        worker = Worker(plugin)
        node.workers.append(worker)
        return worker_jsonify(worker)


worker.add_url_rule('/', view_func=WorkerView.as_view('worker'))

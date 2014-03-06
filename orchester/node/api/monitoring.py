"""
This module is the /monitoring node API
It allows monitoring of all node components

"""

import random

from flask import Blueprint
from flask import url_for, jsonify
from flask.views import MethodView

monitoring = Blueprint('monitoring', __name__)


class MonitoringView(MethodView):
    """
    URL : /monitoring/
    Returns node global metrics

    """
    methods = ['GET']

    def get(self):
        """Returns monitoring data"""
        from orchester.node import node
        metrics = node.get_metrics()
        data = {
            'metrics': metrics,
            'count': len(metrics)
            }
        return jsonify(data)


class MonitoringWorkerView(MethodView):
    """
    URL: /monitoring/worker/<id>
    Return worker specific metrics

    """
    methods = ['GET']

    def get(self, wkr_id):
        """Returns worker <wkr_id> monitoring data"""
        data = {
            'id': wkr_id,
            'url': url_for('worker.worker_get', _external=True, id=wkr_id),
            'metrics': [
                {'name': "mem_free",
                 'value': random.randrange(10, 300),
                 'unit': "MB"},
                {'name': "cpu_usage",
                 'value': random.randrange(0, 100),
                 'unit': "%"},
                ]
            }
        return jsonify(data)


monitoring.add_url_rule('/', 'index', MonitoringView.as_view('index'))
monitoring.add_url_rule('/<wkr_id>', 'worker', MonitoringWorkerView.as_view('worker'))

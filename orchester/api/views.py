"""
Misc utils views for orchester API

"""

from flask import jsonify

from orchester.api import api_version


def index(service, version, capabilities=[], api_version=api_version):
    """
    This is the API root endpoint for orchester services
    This helper function provide a standardized JSON rendering

    """
    data = {
        'service': service,
        'capabilities':  capabilities,
        'version': version,
        'api_version': api_version,
    }
    return jsonify(data)

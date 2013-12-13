"""
This module contains all the tests for the node API

"""

import unittest

from flask import json

from orchester import node

class NodeAPITestCase(unittest.TestCase):
    """
    Base API test case

    Setup the tests context

    """

    def setUp(self):
        self.app = node.app.test_client()


class IndexTestCase(NodeAPITestCase):
    """
    Test the node API root endpoint for correct infos

    """

    def test_status_code(self):
        rv = self.app.get('/')
        assert rv.status_code == 200

    def test_service_type(self):
        rv = self.app.get('/')
        data = json.loads(rv.data)
        assert data.has_key('service')
        assert data['service'] == 'node'

    def test_versions(self):
        rv = self.app.get('/')
        data = json.loads(rv.data)
        assert data.has_key('version')
        assert data.has_key('api_version')


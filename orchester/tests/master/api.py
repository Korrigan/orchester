"""
This module contains all the tests for the master API

"""

import unittest

from flask import json

from orchester import master

class MasterAPITestCase(unittest.TestCase):
    """
    Base API test case

    Setup the tests context

    """

    def setUp(self):
        self.app = master.app.test_client()


class IndexTestCase(MasterAPITestCase):
    """
    Test the master API root endpoint for correct infos

    """

    def test_status_code(self):
        rv = self.app.get('/')
        assert rv.status_code == 200

    def test_service_type(self):
        rv = self.app.get('/')
        data = json.loads(rv.data)
        assert data.has_key('service')
        assert data['service'] == 'master'

    def test_versions(self):
        rv = self.app.get('/')
        data = json.loads(rv.data)
        assert data.has_key('version')
        assert data.has_key('api_version')


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
    database = 'orchester_test'

    def setUp(self):
        master.setup(db_name=self.database)
        self.app = master.app.test_client()
    
    def tearDown(self):
        from pymongo import MongoClient

        c = MongoClient()
        c.drop_database(self.database)


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


class AppTestMixin(object):
    """
    Base class providing utilities for app testing

    """

    def create_app(self, **kwargs):
        """Creates an application and returns the post return"""
        req = {'domain_name': 'example.com',
               'code_type': 'python',
               'code_tag': 'test',
               'code_url': 'https://example.com/repo.git',
               'min_workers': 0,
               'max_workers': 0,
           }
        for (k, v) in kwargs.iteritems():
            req[k] = v
        return self.app.post('/app/', content_type='application/json', data=json.dumps(req))


class AppCreateTestCase(MasterAPITestCase, AppTestMixin):
    """
    Test the /app master API endpoint for app creation

    """

    def test_app_create(self):
        rv = self.create_app()
        assert rv.status_code == 302 or rv.status_code == 301
        json.loads(rv.data)

    def test_app_create_invalid(self):
        req = {'code_type': 'python',
               'code_tag': 'test',
               'max_workers': 0,
           }
        rv = self.app.post('/app/', content_type='application/json', data=json.dumps(req))
        assert rv.status_code == 400


class AppListTestCase(MasterAPITestCase, AppTestMixin):
    """
    Test the listing feature of the /app/ endpoint
    
    """

    def test_app_list(self):
        self.create_app()
        rv = self.app.get('/app/')
        assert rv.status_code == 200
        data = json.loads(rv.data)
        assert data.has_key('count')
        assert data.has_key('apps')
        assert data['count'] != 0
        assert len(data['apps']) == data['count']


class AppDetailTesstCase(MasterAPITestCase, AppTestMixin):
    """
    Tests the detail app API endpoint /app/<app_id>

    """
    def test_app_detail(self):
        rv = self.create_app()
        data = json.loads(rv.data)
        rv = self.app.get(data['url'])
        data = json.loads(rv.data)
        assert data.has_key('id')
        assert data.has_key('domain_name')
        assert data.has_key('min_workers')
        assert data.has_key('max_workers')
        assert data.has_key('code_type')
        assert data.has_key('code_url')
        assert data.has_key('code_tag')
        assert data.has_key('public_key')
        assert data.has_key('env_vars')

    def test_app_update(self):
        rv = self.create_app()
        data = json.loads(rv.data)
        req = {'domain_name': 'example.com',
               'code_type': 'perl',
               'code_tag': 'test',
               'code_url': 'https://example.com/repo.git',
               'min_workers': 0,
               'max_workers': 0,
           }
        rv = self.app.put(data['url'], data=json.dumps(req))
        rv = self.app.get(data['url'])
        data = json.loads(rv.data)
        assert data['code_type'] == 'perl'

    def test_app_update_invalid(self):
        rv = self.create_app()
        data = json.loads(rv.data)
        req = {'code_tag': 'test',
               'max_workers': 0,
           }
        rv = self.app.put(data['url'], data=json.dumps(req))
        assert rv.status_code == 400

    def test_app_delete(self):
        rv = self.create_app()
        data = json.loads(rv.data)
        rv = self.app.delete(data['url'])
        json.loads(rv.data)
        rv = self.app.get(data['url'])
        assert rv.status_code == 404

from flask_testing import TestCase
# from flask_api import FlaskAPI
import unittest
from main import app as flask_app
from nose.tools import set_trace
import json

class test_company(TestCase):
    def create_app(self):
        app = flask_app
        app.config['TESTING'] = True
        return app

    def test_1_get_all_company(self):
        response = self.client.get('/company')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.data)['data']), 251)

    def test_2_get_company_name(self):
        response = self.client.get('/company?company_name=ben%20tre%20aquaproduct')
        self.assertEqual(response.status_code, 200)

    def test_3_get_industry(self):
        response = self.client.get('/company?industry="Food Processing"')
        self.assertEqual(response.status_code, 200)

    def test_4_get_revenue(self):
        response = self.client.get('/company?revenue_gte=3800000000000')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.data)['data']), 1)

    def test_5_failed_response(self):
        response = self.client.get('/company?revenue_gte=x')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data)['status_code'], 400)

if __name__ == '__main__':
    unittest.main()
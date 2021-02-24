import unittest
from django.test import Client

class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.client = Client()

    def test_details(self):
        # Create an instance of a GET request.
        response = self.client.get('/msgs/')
        self.assertEqual(response.status_code, 403)
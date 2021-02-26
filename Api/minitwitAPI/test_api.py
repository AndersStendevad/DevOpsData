import unittest
from django.test import Client
import base64
import json

class SimpleTest(unittest.TestCase):

    BASE_URL = "http://localhost:8080"
    USERNAME = "simulator"
    PWD = "super_safe!"
    CREDENTIALS = ":".join([USERNAME, PWD]).encode("ascii")
    ENCODED_CREDENTIALS = base64.b64encode(CREDENTIALS).decode()
    HEADERS = {
        "Connection": "close",
        "Content-Type": "application/json",
        f"Authorization": f"Basic {ENCODED_CREDENTIALS}",
    }

    def setUp(self):
        # Every test needs access to the request factory.
        self.client = Client()

    def test_details(self):
        # Create an instance of a GET request.
        response = self.client.get('/msgs/')
        self.assertEqual(response.status_code, 403)

    def test_latest(self):
        url = "/register/?latest=1337"
        data = {"username": "test", "email": "test@test", "pwd": "foo"}
        response = self.client.post(url, data, content_type='application/json', HEADERS=self.HEADERS)
        self.assertEqual(response.status_code, 204)
       
           
        url = "/latest/"
        response = self.client.get(url, HEADERS=self.HEADERS)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["latest"], '1337')


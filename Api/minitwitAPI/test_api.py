import unittest
from django.test import Client
import base64
import json

class SimpleTest(unittest.TestCase):

    BASE_URL = "http://127.0.0.1:8000"
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
        self.client = Client()

    def test_details(self):
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

    def test_register(self):
        url = "/register/?latest=1"
        username = "a"
        email = "a@a.a"
        pwd = "a"
        data = {"username": username, "email": email, "pwd": pwd}

        response = self.client.post(url, data, content_type='application/json', HEADERS=self.HEADERS)
        self.assertEqual(response.status_code, 204)

        url = '/msgs/a'
        response = self.client.get(url, HEADERS=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        url = '/latest/'
        response = self.client.get('/latest', HEADERS=self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], '1')


    def test_create_msg(self):
        username = "a"
        url = f"/msgs/{username}/?latest=2"
        data = {"content": "Blub!"}
        response = self.client.post(url, data, content_type='application/json', HEADERS=self.HEADERS)
        self.assertEqual(response.status_code, 204)

        url = "/latest/"
        response = self.client.get(url, HEADERS=self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], '2')

    def test_get_latest_user_msgs(self):
        username = "a"
        url = "/msgs/{username}/?no=20&latest=3"
        response = self.client.get(url, headers=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        got_it_earlier = False
        for msg in json.loads(response.text):
            if msg["content"] == "Blub!" and msg["user"] == username:
                got_it_earlier = True

        self.assertEqual(got_it_earlier, True)

        response = self.client.get("/latest/", headers=self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], '3')

    def test_get_latest_msgs(self):
        username = "a"
        url = "/msgs/?no=20&latest=4"
        response = self.client.get(url, headers=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        got_it_earlier = False
        for msg in json.loads(response.text):
            if msg["content"] == "Blub!" and msg["user"] == username:
                got_it_earlier = True

        self.assertEqual(got_it_earlier, True)

        # verify that latest was updated
        response = self.client.get("/latest/", headers=self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], '4')

    def test_register_b(self):
        url = '/register/?latest=5'
        username = "b"
        email = "b@b.b"
        pwd = "b"
        data = {"username": username, "email": email, "pwd": pwd}
        response = self.client.post(url, data, content_type='application/json', headers=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        url = '/msgs/b'
        response = self.client.get(url, HEADERS=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        url = '/latest/'
        response = self.client.get('/latest', HEADERS=self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], '5')

    def test_register_b(self):
        url = '/register/?latest=6'
        username = "b"
        email = "b@b.b"
        pwd = "b"
        data = {"username": username, "email": email, "pwd": pwd}
        response = self.client.post(url, data, content_type='application/json', headers=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        url = '/msgs/c'
        response = self.client.get(url, HEADERS=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        url = '/latest/'
        response = self.client.get('/latest', HEADERS=self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], '6')

    def test_follow_user(self):
        username = "a"
        url = f"/fllws/{username}/?latest=7"
        data = {"follow": "b"}
        response = self.client.post(url, data, content_type='application/json', headers=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        url = f"/fllws/{username}/?latest=8"
        data = {"follow": "c"}
        response = self.client.post(url, data, content_type='application/json', headers=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        url = f"/fllws/{username}/?no=20&latest=9"
        response = self.client.get(url, headers=self.HEADERS, params=query)
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.text)
        self.assertEqual(json.loads(response.content)["follows"], 'b')
        self.assertEqual(json.loads(response.content)["follows"], 'c')

        response = self.client.get('/latest', HEADERS=self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], '9')

    def test_a_unfollows_b(self):
        username = "a"
        url = f"/fllws/{username}/?latest=10"

        data = {"unfollow": "b"}
        response = self.client.post(url, data, content_type='application/json', headers=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        url = f"/fllws/{username}/?no=20&latest=11"
        response = self.client.post(url, content_type='application/json', headers=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.text)
        unfollowed = False
        if 'b' not in json.loads(response.content)["follows"]:
            unfollowed = True
        self.assertEqual(unfollowed, True)

        response = self.client.get('/latest', HEADERS=self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], '11')
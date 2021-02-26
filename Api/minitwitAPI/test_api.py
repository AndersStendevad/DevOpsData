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
        "Authorization": f"Basic {ENCODED_CREDENTIALS}",
    }

    def setUp(self):
        self.client = Client()

    def test_details(self):
        response = self.client.get("/msgs/")
        self.assertEqual(response.status_code, 403)

    def test_latest(self):
        data = {"username": "test", "email": "test@test", "pwd": "foo"}
        response = self.client.post(
            "/register?latest=1337",
            data,
            content_type="application/json",
            HEADERS=self.HEADERS,
        )
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/latest/", HEADERS=self.HEADERS)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["latest"], "1337")

    def test_register(self):
        data = {"username": "a", "email": "a@a.a", "pwd": "a"}

        response = self.client.post(
            "/register?latest=1",
            data,
            content_type="application/json",
            HEADERS=self.HEADERS,
        )
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/msgs/a", HEADERS=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/latest/", HEADERS=self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], "1")

        self.Test_create_msg()
        self.Test_get_latest_user_msgs()
        self.Test_get_latest_msgs()
        self.Test_register_c()
        self.Test_follow_user()
        self.Test_a_unfollows_b()

    def Test_create_msg(self):
        data = {"content": "Blub!"}
        response = self.client.post(
            "/msgs/a?latest=2",
            data,
            content_type="application/json",
            HEADERS=self.HEADERS,
        )
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/latest/", HEADERS=self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], "2")

    def Test_get_latest_user_msgs(self):
        response = self.client.get("/msgs/a?no=20&latest=3", HEADERS=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        got_it_earlier = False
        for msg in json.loads(response.text):
            if msg["content"] == "Blub!" and msg["user"] == username:
                got_it_earlier = True

        self.assertEqual(got_it_earlier, True)

        response = self.client.get("/latest/", HEADERS=self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], "3")

    def Test_get_latest_msgs(self):
        response = self.client.get("/msgs?no=20&latest=4", HEADERS=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        got_it_earlier = False
        for msg in json.loads(response.text):
            if msg["content"] == "Blub!" and msg["user"] == "a":
                got_it_earlier = True

        self.assertEqual(got_it_earlier, True)

        response = self.client.get("/latest/", HEADERS=self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], "4")

    def test_register_b(self):
        data = {"username": "b", "email": "b@b.b", "pwd": "b"}
        response = self.client.post(
            "/register?latest=5",
            data,
            content_type="application/json",
            HEADERS=self.HEADERS,
        )
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/msgs/b", HEADERS=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/latest/", HEADERS=self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], "5")

    def Test_register_c(self):
        data = {"username": "c", "email": "c@c.c", "pwd": "c"}
        response = self.client.post(
            "/register?latest=6",
            data,
            content_type="application/json",
            HEADERS=self.HEADERS,
        )
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/msgs/c", HEADERS=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/latest/", HEADERS=self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], "6")

    def Test_follow_user(self):
        data = {"follow": "b"}
        response = self.client.post(
            "/fllws/a?latest=7",
            data,
            content_type="application/json",
            HEADERS=self.HEADERS,
        )
        self.assertEqual(response.status_code, 200)

        data = {"follow": "c"}
        response = self.client.post(
            "/fllws/a?latest=8",
            data,
            content_type="application/json",
            HEADERS=self.HEADERS,
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/fllws/a?no=20&latest=9", HEADERS=self.HEADERS)
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.text)
        self.assertEqual(json.loads(response.content)["follows"], "b")
        self.assertEqual(json.loads(response.content)["follows"], "c")

        response = self.client.get("/latest/", HEADERS=self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], "9")

    def Test_a_unfollows_b(self):
        data = {"unfollow": "b"}
        response = self.client.post(
            "/fllws/a?latest=10",
            data,
            content_type="application/json",
            HEADERS=self.HEADERS,
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/fllws/a?no=20&latest=11",
            content_type="application/json",
            HEADERS=self.HEADERS,
        )
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.text)
        unfollowed = False
        if "b" not in json.loads(response.content)["follows"]:
            unfollowed = True
        self.assertEqual(unfollowed, True)

        response = self.client.get("/latest/", HEADERS=self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], "11")

import unittest
from django.test import Client
import base64
import json


class SimpleTest(unittest.TestCase):

    USERNAME = "simulator"
    PWD = "super_safe!"
    CREDENTIALS = ":".join([USERNAME, PWD]).encode("ascii")
    ENCODED_CREDENTIALS = base64.b64encode(CREDENTIALS).decode()
    HEADERS = {
        "Connection": "close",
        "HTTP_AUTHORIZATION": f"Basic {ENCODED_CREDENTIALS}",
    }

    def setUp(self):
        self.client = Client()

    def test_1_latest(self):
        data = {"username": "test", "email": "test@test", "pwd": "foo"}
        response = self.client.post(
            "/register?latest=1337",
            data,
            content_type="application/json",
            **self.HEADERS,
        )
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/latest/", **self.HEADERS)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["latest"], "1337")

    def test_2_register(self):
        data = {"username": "a", "email": "a@a.a", "pwd": "a"}

        response = self.client.post(
            "/register?latest=1",
            data,
            content_type="application/json",
            **self.HEADERS,
        )
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/msgs/a", **self.HEADERS)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/latest/", **self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], "1")

    def test_3_create_msg(self):
        data = {"content": "Blub!"}
        response = self.client.post(
            "/msgs/a?latest=2",
            data,
            content_type="application/json",
            **self.HEADERS,
        )
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/latest/", **self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], "2")

    def test_4_get_latest_user_msgs(self):
        response = self.client.get("/msgs/a?no=20&latest=3", **self.HEADERS)
        self.assertEqual(response.status_code, 200)

        got_it_earlier = False
        for msg in response.json():
            if msg["content"] == "Blub!" and msg["user"] == "a":
                got_it_earlier = True

        self.assertEqual(got_it_earlier, True)

        response = self.client.get("/latest/", **self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], "3")

    def test_5_get_latest_msgs(self):
        response = self.client.get("/msgs/?no=20&latest=4", **self.HEADERS)
        self.assertEqual(response.status_code, 200)

        got_it_earlier = False
        for msg in response.json():
            if msg["content"] == "Blub!" and msg["user"] == "a":
                got_it_earlier = True

        self.assertEqual(got_it_earlier, True)

        response = self.client.get("/latest/", **self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], "4")

    def test_6_register_b(self):
        data = {"username": "b", "email": "b@b.b", "pwd": "b"}
        response = self.client.post(
            "/register?latest=5",
            data,
            content_type="application/json",
            **self.HEADERS,
        )
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/msgs/b", **self.HEADERS)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/latest/", **self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], "5")

    def test_7_register_c(self):
        data = {"username": "c", "email": "c@c.c", "pwd": "c"}
        response = self.client.post(
            "/register?latest=6",
            data,
            content_type="application/json",
            **self.HEADERS,
        )
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/msgs/c", **self.HEADERS)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/latest/", **self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], "6")

    def test_8_follow_user(self):
        data = {"follow": "b"}
        response = self.client.post(
            "/fllws/a?latest=7",
            data,
            content_type="application/json",
            **self.HEADERS,
        )
        self.assertEqual(response.status_code, 204)

        data = {"follow": "c"}
        response = self.client.post(
            "/fllws/a?latest=8",
            data,
            content_type="application/json",
            **self.HEADERS,
        )
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/fllws/a?no=20&latest=9", **self.HEADERS)
        self.assertEqual(response.status_code, 200)

        check_b_in = False
        check_c_in = False
        if "b" in json.loads(response.content)["follows"]:
            check_b_in = True
        if "c" in json.loads(response.content)["follows"]:
            check_c_in = True
        self.assertEqual(check_b_in, True)
        self.assertEqual(check_c_in, True)

        response = self.client.get("/latest/", **self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], "9")

    def test_9_a_unfollows_b(self):
        data = {"unfollow": "b"}
        response = self.client.post(
            "/fllws/a?latest=10",
            data,
            content_type="application/json",
            **self.HEADERS,
        )
        self.assertEqual(response.status_code, 204)

        response = self.client.get(
            "/fllws/a?no=20&latest=11",
            **self.HEADERS,
        )

        self.assertEqual(response.status_code, 200)

        unfollowed = False
        if "b" not in json.loads(response.content)["follows"]:
            unfollowed = True
        self.assertEqual(unfollowed, True)

        response = self.client.get("/latest/", **self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], "11")

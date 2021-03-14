from django.test import Client, TestCase
import base64
import json


class SimpleTest(TestCase):

    USERNAME = "simulator"
    PWD = "super_safe!"
    CREDENTIALS = ":".join([USERNAME, PWD]).encode("ascii")
    ENCODED_CREDENTIALS = base64.b64encode(CREDENTIALS).decode()
    HEADERS = {
        "Connection": "close",
        "HTTP_AUTHORIZATION": f"Basic {ENCODED_CREDENTIALS}",
    }

    def register_user(self, username, email, pwd, latest):
        data = {"username": username, "email": email, "pwd": pwd}
        response = self.client.post(
            f"/register?latest={latest}",
            data,
            content_type="application/json",
            **self.HEADERS,
        )
        return response

    def msg_user(self, user, message, latest):
        data = {"content": f"{message}"}
        response = self.client.post(
            f"/msgs/{user}?latest={latest}",
            data,
            content_type="application/json",
            **self.HEADERS,
        )
        return response

    def latest_msg_user(self, user, no, latest):
        response = self.client.get(f"/msgs/{user}?no={no}&latest={latest}", **self.HEADERS)
        return response

    def latest_msg(self, no, latest):
        response = self.client.get(f"/msgs/?no={no}&latest={latest}", **self.HEADERS)
        return response

    def follow_user(self, base_user, follow, latest):
        data = {"follow": follow}
        response = self.client.post(
            f"/fllws/{base_user}?latest={latest}",
            data,
            content_type="application/json",
            **self.HEADERS,
        )
        return response

    def unfollow_user(self, base_user, unfollow, latest):
        data = {"unfollow": unfollow}
        response = self.client.post(
            f"/fllws/{base_user}?latest={latest}",
            data,
            content_type="application/json",
            **self.HEADERS,
        )
        return response

    def test_1_latest(self):
        response = self.register_user("test", "test@test", "foo", 1337)
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/latest/", **self.HEADERS)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["latest"], 1337)

    def test_2_register(self):
        response = self.register_user("a", "a@a.a", "a", 1)
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/msgs/a", **self.HEADERS)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/latest/", **self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], 1)

    def test_3_create_msg(self):
        self.register_user("a", "a@a.a", "a", 1)
        response = self.msg_user("a", "Blub!", 2)
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/latest/", **self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], 2)

    def test_4_get_latest_user_msgs(self):
        self.register_user("a", "a@a.a", "a", 1)
        self.msg_user("a", "Blub!", 2)

        response = self.latest_msg_user("a", 20, 3)
        self.assertEqual(response.status_code, 200)

        got_it_earlier = False
        for msg in response.json():
            if msg["content"] == "Blub!" and msg["user"] == "a":
                got_it_earlier = True

        self.assertEqual(got_it_earlier, True)

        response = self.client.get("/latest/", **self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], 3)

    def test_5_get_latest_msgs(self):
        self.register_user("a", "a@a.a", "a", 1)
        self.msg_user("a", "Blub!", 2)
        response = self.latest_msg(20, 4)
        self.assertEqual(response.status_code, 200)

        got_it_earlier = False
        for msg in response.json():
            if msg["content"] == "Blub!" and msg["user"] == "a":
                got_it_earlier = True

        self.assertEqual(got_it_earlier, True)

        response = self.client.get("/latest/", **self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], 4)

    def test_6_register_b(self):
        response = self.register_user("b", "b@b.b", "b", 5)
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/msgs/b", **self.HEADERS)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/latest/", **self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], 5)

    def test_7_register_c(self):
        response = self.register_user("c", "c@c.c", "c", 6)
        self.assertEqual(response.status_code, 204)

        response = self.client.get("/msgs/c", **self.HEADERS)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/latest/", **self.HEADERS)
        self.assertEqual(json.loads(response.content)["latest"], 6)

    def test_8_follow_user(self):
        self.register_user("a", "a@a.a", "a", 1)
        self.register_user("b", "b@b.b", "b", 5)
        self.register_user("c", "c@c.c", "c", 6)

        response = self.follow_user("a", "b", 7)
        self.assertEqual(response.status_code, 204)

        response = self.follow_user("a", "c", 8)
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
        self.assertEqual(json.loads(response.content)["latest"], 9)

    def test_9_a_unfollows_b(self):
        self.register_user("a", "a@a.a", "a", 1)
        self.register_user("b", "b@b.b", "b", 5)
        self.register_user("c", "c@c.c", "c", 6)
        self.follow_user("a", "b", 7)
        self.follow_user("a", "c", 8)
        
        response = self.unfollow_user("a", "b", 10)
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
        self.assertEqual(json.loads(response.content)["latest"], 11)

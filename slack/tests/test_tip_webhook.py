from django.test import TestCase, Client


class TestTipWebHook(TestCase):

    def test_redirects(self):
        c = Client()
        self.assertEqual(c.get("/").status_code, 301)
        self.assertEqual(c.get("/bob").status_code, 301)

    def test_tip(self):
        post_data = {
            "token": "madeuptoken",
            "team_id": "T0001",
            "channel_id": "C2147483705",
            "channel_name": "test",
            "user_id": "U2147483697",
            "user_name": "Steve",
            "command": "/tip",
            "text": "no text"
        }
        c = Client()
        self.assertEqual(c.get("/command-webhook").status_code, 405)

        response = c.post("/command-webhook", post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(response.content).find("Usage"))

        post_data["text"] = "@tippee $1"
        response = c.post("/command-webhook", post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(response.content).find("Hi"))

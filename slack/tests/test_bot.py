from django.test import TestCase
from bot import SlackBot


class BotTestCase(TestCase):

    def test_unique_id(self):
        bot = SlackBot()
        post_data = {
            "token": "madeuptoken",
            "team_id": "T0001",
            "channel_id": "C2147483705",
            "channel_name": "test",
            "user_id": "U2147483697",
            "user_name": "Steve",
            "command": "/tip",
            "text": "@tippee $1"
        }

        hash1 = bot.unique_id(post_data)
        hash2 = bot.unique_id(post_data)
        self.assertEqual(hash1, hash2)

        post_data["text"] = "@tippee $2"
        hash3 = bot.unique_id(post_data)
        self.assertNotEqual(hash1, hash3)

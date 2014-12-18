from changetip.bots.base import BaseBot
import datetime
import hashlib
import os

CHANGETIP_API_KEY = os.getenv("CHANGETIP_API_KEY")
assert CHANGETIP_API_KEY, "CHANGETIP_API_KEY environment variable must be set. To get one, contact support@changetip.com"


class SlackBot(BaseBot):

    channel = "slack"
    changetip_api_key = CHANGETIP_API_KEY

    def unique_id(self, post_data):
        # Generatee a special id to prevent duplicates.
        checksum = hashlib.md5()
        checksum.update(str(post_data).encode("utf8"))

        # Now we also include a time stamp for entry.
        # Note it is to the minute, so that people can send the same tip a little later
        # The idea here is that we want to prevent dupelicates, but not prevent the same tip a minute later
        checksum.update(datetime.datetime.now().strftime('%Y-%m-%d:%H:%M:00').encode("utf8"))

        return checksum.hexdigest()[:16]

from django.core.cache import cache
import logging
import random
import re
import requests

logger = logging.getLogger(__name__)

# Attention. ONLY POSITIVE WORDS ARE TO BE ASSOCIATED WITH CHANGETIP
# Put them in alphabetical order
# Available terms http://giphy.com/categories/
IMAGE_RESPONSE_HASHTAGS = [
    "agree",
    "applause",
    "awesome",
    "awww",
    "cat",
    "cute",
    "dancing",
    "dreaming",
    "drunk",
    "eating",
    "excited",
    "fainting",
    "fistbump",
    "funny",
    "happy",
    "highfive",
    "hungry",
    "hug",
    "inspired",
    "kiss",
    "laughing",
    "lol",
    "love",
    "omg",
    "oops",
    "please",
    "singing",
    "sleeping",
    "smiling",
    "smile",
    "sorry",
    "spinning",
    "squee",
    "success",
    "surprised",
    "wink",
    "win",
    "wow",
    "yes",
]


class ImageResponse(object):

    def get_image_response(self, message, max_size=None):
        try:
            message = " %s " % message # word boundary hack
            match = re.search('\#(' + "|". join(IMAGE_RESPONSE_HASHTAGS) + r')\b', message, re.I)
            if match:
                hashtag = match.group(1).lower()
                if hashtag[0:1] in ["a", "e", "i", "o", "u"]: # sometimes y?
                    a = "an"
                else:
                    a = "a"
                url = self.get_image_response_url(hashtag, max_size)
                return (hashtag, a, url)
        except:
            # Don't let a failed image response break a tip
            logger.exception("Error getting image response")

        return (None, None, None)

    def get_image_response_url(self, mood, max_size):

        def get_urls_from_giphy(keyword, max_size):
            cache_key = "giphy_image_urls:%s" % keyword
            response = cache.get(cache_key)
            api_key = "dc6zaTOxFJmzC" # demo. change this once we get a real one
            if not response:
                response = requests.get("http://api.giphy.com/v1/gifs/search?q=%s&api_key=%s" % (keyword, api_key)).json()
                cache.set(cache_key, response, 30 * 60)
            urls = []
            for listing in response['data']:
                if listing["rating"] not in ["g", "pg"]:
                    continue
                if max_size and int(listing["images"]["original"]["size"]) > max_size:
                    continue
                urls.append(listing["images"]["fixed_height"]["url"])

            return urls

        urls = get_urls_from_giphy(mood, max_size)

        return random.choice(urls)

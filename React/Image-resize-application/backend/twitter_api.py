import tweepy
import os
from config import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def post_to_x(image_path, caption="Here’s my resized image!"):
    """ Posts a given image to X (formerly Twitter) """
    try:
        api.update_status_with_media(status=caption, filename=image_path)
        print(f"Posted: {image_path}")
    except Exception as e:
        print(f"Error posting to X: {e}")

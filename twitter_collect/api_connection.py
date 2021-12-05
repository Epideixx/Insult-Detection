import tweepy
from twitter_collect.credentials import *

"""This Module handles connection to twitter API
"""

def get_api():
    """Generate an API connection with the API key in credentials.py

    Returns:
        API: The Api object generated with the credentials
    """
    
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API with authentication:
    api = tweepy.API(auth,wait_on_rate_limit=True)
    return api

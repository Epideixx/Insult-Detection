import tweepy
from twitter_collect.api_connection import get_api

""" This module handle the queries to
twitter API
"""

api = get_api()

def get_user_tweets(name,nb_tweets):
    """
    Returns last nb_tweets tweets of the target user

    Args:
        name (str): the screen_name of the target user
        nb_tweets (int): the number of tweets to return
    
    Returns:
        list : list of last tweets tweepy.Cursor(api.user_timeline, id="twitter")
    """

    tweets = []
    cursor = tweepy.Cursor(api.user_timeline,screen_name = name, tweet_mode="extended").items(nb_tweets)
    for tweet in cursor:
        tweets.append(tweet)
    return tweets

def get_replies(screen_name,max_queries):

    """
    Returns a list of last replies to a user
    nb: The number of replies may be different from max_queries because of the mentions which are not replies

    Args:
        name (str): the screen_name of the target user
        max_queries (int): maximum number of queries to the api

    Returns:
        list: list of replies to the tweet

    """

    replies = []
    cursor = tweepy.Cursor(api.search, q='to:' + screen_name, tweet_mode = "extended").items(max_queries)
    for reply in cursor:
        if hasattr(reply, 'in_reply_to_status_id'):
            replies.append(reply)
    return replies

def get_nb_followers(screen_name):
    try:
        return api.get_user(screen_name).followers_count
    except tweepy.error.TweepError:
        return 0

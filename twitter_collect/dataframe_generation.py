import pandas as pd
from twitter_collect.api_queries import get_user_tweets,get_replies,get_nb_followers

"""This module handles the generation of a dataframe containing replies to the tweets of a user
"""

def get_dataframe(screen_name,nb_tweets = 20,max_queries = 500):
    """Returns a dataframe containing replies to the last tweets of the user screen_name

    Args:
        screen_name (string): screen_name of the target user
        nb_tweets (int): number of tweets from the user to consider
        max_queries (int): maximum number of call to the api used to prevent blockage from twitter api
    """

    data = []
    if nb_tweets + max_queries >= 900:
        print("WARNING: Over 900 queries requested, expect high delay in generation")
    tweets_id = [tweet.id for tweet in get_user_tweets(screen_name,nb_tweets)]
    replies = get_replies(screen_name,max_queries)
    for reply in replies:
        if reply.in_reply_to_status_id in tweets_id:
            tweet_dict = {"user": reply.user.screen_name,
                "text": reply.full_text,
                "date": pd.to_datetime(str(reply.created_at),format='%Y-%m-%d %H:%M:%S'),
                "id": reply.id,
                "likes":reply.favorite_count,
                "retweets":reply.retweet_count,
                "reply_to":reply.in_reply_to_status_id,
                "followers":get_nb_followers(reply.user.screen_name)}
            data.append(tweet_dict)
    return pd.DataFrame(data)
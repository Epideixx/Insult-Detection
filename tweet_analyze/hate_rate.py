from textblob import TextBlob
from tweet_analyze.dictionnary_treatment import *
from tweet_analyze.nlp_V1 import analyse_nlp1


def analyse_tweets(tweets):
    """ 
    This function add a 'hate_rate' to the dataframe; this hate_rate is a float
    between -1 and 1 (1 is hatefull) is calculated whith textblob.

    Args:
        tweets (dataframe): tweets from hate_rate
    Return:
        dataframe with a new colomn of floats in [-1,1] which are a first hate_rate calculated with textblob 
    """

    hate_rate = []
    for tweet in tweets["text"]:
        text = TextBlob(tweet)
        pol = text.sentiment.polarity
        if pol != 0.0:
            hate_rate.append(-pol)
        else:
            hate_rate.append(pol)

    tweets["hate_rate"] = hate_rate

    return tweets

def average_hate(tweets):
    """ 
    Calculates an average of the differents hate rates returned by dictionnary_treatment
    and nlp_V1

    Args:
        tweets (dataframe): tweets from hate_rate
    Return:
        dataframe with a new colomn of float in [0,1] which represent the average hate rate of the tweets
    """
    dic = analyse_bis(analyse_tweets(tweets), 0.1)
    nlp = analyse_nlp1(tweets)
    avrg_hate = []
    (l,c) = dic.shape
    
    #Calcul of the weighted average
    for i in range(l):
        if dic["insult"][i]:
            avrg_hate.append((0.2*((dic["hate_rate"][i] + 1)/2) + 0.8*(nlp['nlp1_insult_estimation'][i]) + 0.2)/1.2)
        else:
            avrg_hate.append(0.2*((dic["hate_rate"][i] + 1)/2) + 0.8*(nlp['nlp1_insult_estimation'][i]))
            
    #Add the new colomn to the dataframe
    tweets["avrg_hate"] = avrg_hate

    return tweets
# Second traitement thanks to a dictionnary of insults

import pandas as pd
from nltk.corpus import stopwords
from textblob import TextBlob, Word
from textblob.wordnet import VERB
import nltk
nltk.download('stopwords')


def analyse_bis(tweets, treshold=0):
    """
    Makes a second selection thanks to a dictionnary of insults

    Args:
        tweets (dataframe): tweets from hate_rate
        treshold (float): minimum hateful rate of a tweet
    Returns:
        dataframe : dataframe with a new column (insulting: True/False)
    """

    # Creation of the list of insults
    dictionnary = pd.read_csv(
        "tweet_analyze/list_of_insults.csv", delimiter=";")

    list_insult = [row for row in dictionnary.insult]

    # Prepares to add an "insult" column (True/False)
    insult_column = []
    counter = 0

    # For each tweet
    for tweet in tweets["text"]:
        insult = False

        # Selection of the estimated enoughtly hateful texts
        if tweets["hate_rate"][counter] == 0 or tweets["hate_rate"][counter] >= treshold:
            message = TextBlob(tweet)

            # Removes the stopwords and added stopwords "great" and "good"
            vocab = []
            stop_words_added = ["great", "good", "Great", "Good"]
            for word in message.words:
                if (word not in stopwords.words('english')) and (word not in stop_words_added):
                    vocab.append(word.lemmatize())

            # Matching between the insulting list and the tweet text
            for word in vocab:
                if word in list_insult:
                    insult = True
                    break

        insult_column.append(insult)
        counter += 1

    # Adds an "insult" column(True/False)
    tweets["insult"] = insult_column

    return tweets


def analyse_bis2(tweets, treshold=0):
    """
    Makes a second selection thanks to a dictionnary of insults

    Args:
        tweets (dataframe): tweets from hate_rate
        treshold (float): minimum hateful rate of a tweet
    Returns:
        dataframe : dataframe with a new column (insulting_quantity_lvl: [0,3])
    """

    # Creation of the list of insults
    dictionnary = pd.read_csv(
        "tweet_analyze/list_of_insults.csv", delimiter=";")

    list_insult = [row for row in dictionnary.insult]

    # Prepares to add an "insult" column (True/False)
    insult_column = []
    counter = 0

    # For each tweet
    for tweet in tweets["text"]:
        insult = 0

        # Selection of the estimated enoughtly hateful texts
        if tweets["hate_rate"][counter] == 0 or tweets["hate_rate"][counter] >= treshold:
            message = TextBlob(tweet)

            # Removes the stopwords and added stopwords "great" and "good"
            vocab = []
            stop_words_added = ["great", "good", "Great", "Good"]
            for word in message.words:
                if (word not in stopwords.words('english')) and (word not in stop_words_added):
                    vocab.append(word.lemmatize())

            # Matching between the insulting list and the tweet text

            for word in vocab:
                if word in list_insult:
                    insult += 1
                    if insult >= 5:
                        break
        if insult == 0:
            insult_rate = 0
        elif insult == 1:
            insult_rate = 1
        elif insult > 1 and insult <= 4:
            insult_rate = 2
        else:
            insult_rate = 3

        insult_column.append(insult_rate)
        counter += 1

    # Adds an "insult" column(True/False)
    tweets["insult_quantity_lvl"] = insult_column

    return tweets

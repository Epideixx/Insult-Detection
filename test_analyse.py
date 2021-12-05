import json
from tweet_analyze import *
import pandas as pd
import os

# Test of the analyse block

path_to_StoredData = os.path.join(
    os.path.abspath(__file__ + "/../"), "Data")

dataframe = pd.read_json(os.path.join(path_to_StoredData,
                                      "realDonaldTrump.json"), orient="records")

if __name__ == "__main__":
    print(dataframe)
    print(analyse_tweets(dataframe))
    print(analyse_bis(analyse_tweets(dataframe), 0.1))
    print(analyse_bis2(analyse_tweets(dataframe), 0.1))
    print(analyse_nlp1(dataframe))
    print(average_hate(dataframe))

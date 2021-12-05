import seaborn as sns
import matplotlib.pyplot as plt
from tweet_analyze import *

#fonction qui retourne la figure de la premiere analyse
def affichage_prem (tweets):   
    sns.set()               #ou sns.set_theme()  cela dépend de la version de seaborn installée

    # visualition des données
    sns.jointplot(data=analyse_tweets(tweets), x="date", y="hate_rate")

    return plt.figure()


#fonction qui retourne la figure de la deuxieme analyse
def affichage_deu(tweets):  
    sns.set()               #ou sns.set_theme()  cela dépend de la version de seaborn installée

    # visualition des données
    sns.jointplot(data=analyse_bis(tweets,0.2), x="date", y="hate_rate",hue="insult")

    return plt.figure()
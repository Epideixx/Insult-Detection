# This module contains different types of approximations
# NOTE : after thinking of the polynomial approximation, the other ones may ont be really usefull...

from math import exp, log
import numpy as np
import matplotlib.pyplot as plt
import json
from tweet_analyze import analyse_tweets, analyse_bis
import pandas as pd
import os
from datetime import datetime


def collect_coordonates(dataf):
    """
        Gives the coordonates used by the next functions

        Args:
            dataf (dataframe): dataframe of tweets

        Returns:
            (tuple): dates(list), hate_rates(list)
    """

    analyzed_dataf = analyse_bis(analyse_tweets(dataf), 0.1)
    x, y = [], []
    (l, _) = analyzed_dataf.shape
    for i in range(l):
        if analyzed_dataf["insult"][i]:
            x.append(datetime.timestamp(analyzed_dataf["date"][i]))
            y.append(analyzed_dataf["hate_rate"][i])

    return x, y


def linear_approximation(X, Y):
    """
    Returns a linear function which approximates the curve

    Args:
        X(list): List of the abs points
        Y(list): List of the ord points

    Returns:
        function: linear function
    """
    avrg_X, avrg_X2, avrg_Y, avrg_XY = 0, 0, 0, 0
    n = len(X)
    for i in range(n):
        avrg_X += X[i] / n
        avrg_X2 += X[i] ** 2 / n
        avrg_Y += Y[i] / n
        avrg_XY += X[i]*Y[i] / n

    try:
        a = (avrg_XY - avrg_X * avrg_Y) / (avrg_X2 - (avrg_X)**2)
        b = avrg_Y - a*avrg_X

        def linear(x):
            return a*x + b

        return linear

    except ZeroDivisionError:
        print("Une erreur est survenue lors de la régression linéaire car il n'y a qu'une valeur")

        def function(x):
            return Y[0]

        return function


def exponential_approximation(X, Y):
    """
    Returns an exponential function which approximates the curve

    Args:
        X(list): List of the abs points
        Y(list): List of the ord points

    Returns:
        function: exponential function
    """
    logY = []
    for y in Y:
        if y <= 0:
            logY.append(log(0.0000000001))
        else:
            logY.append(log(y))

    def exponential(x):
        return(exp(linear_approximation(X, logY)(x)))

    return exponential


def polynomial_approximation(X, Y, deg=2):
    """
    Returns a polynomial function of degre 'deg' which approximates the curve

    Args:
        X(list): List of the abs points
        Y(list): List of the ord points
        deg(int): degre of the approximation function

    Returns:
        function: polynomial function
    """
    return np.poly1d(np.polyfit(X, Y, deg))


def best_approximation(X, Y):
    """ 
    Enables to know which function best approximates the curve

    Args:
        X(list): abscissa
        Y(list): ordinate

    Returns:
        function : function which is the best approximation
    """

    Y_dict = {}
    Y_dict['lin'] = [linear_approximation(X, Y)(x) for x in X]
    Y_dict['exp'] = [exponential_approximation(X, Y)(x) for x in X]
    Y_dict['poly2'] = [polynomial_approximation(X, Y, 2)(x) for x in X]
    Y_dict['poly4'] = [polynomial_approximation(X, Y, 4)(x) for x in X]
    Y_dict['poly6'] = [polynomial_approximation(X, Y, 6)(x) for x in X]

    ecart = {}
    ecart["lin"] = 0
    ecart["exp"] = 0
    ecart["poly2"] = 0
    ecart["poly4"] = 0
    ecart["poly6"] = 0

    for i in range(len(Y)):
        for key in ecart.keys():
            ecart[key] += (Y[i] - Y_dict[key][i])**2

    best, _ = min(ecart.items(), key=lambda x: x[1])

    if best == "lin":
        return linear_approximation(X, Y)
    elif best == "exp":
        return exponential_approximation(X, Y)
    elif best == "poly2":
        return polynomial_approximation(X, Y, 2)
    elif best == "poly4":
        return polynomial_approximation(X, Y, 4)
    else:
        return polynomial_approximation(X, Y, 6)

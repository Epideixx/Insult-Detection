# Natural Langage Processing in order to better filter tweets

import random
from pathlib import Path
import thinc.extra.datasets
import spacy
from spacy.util import minibatch, compounding
import os
import random
import pandas as pd


def load_data(file="tweet_analyze/train_nlp1.csv", split=0.8, limit=0):
    """
    Loads data from the file of offensing comments

    Args:
        file(str): relative pathway to access the file
        split(float): in [0,1] to split the data in a training set and a test set
        limit(int): maximum of tweets

    Returns:
        tuple : training set and test set

    """
    f = pd.read_csv(file, delimiter=",")
    df = f.sample(frac=1).reset_index(drop=True)
    texts, insults = df["Comment"][-limit:], df["Insult"][-limit:]
    cats = [{'INSULTING': bool(y)} for y in insults]
    split = int(len(texts)*split)
    return (texts[:split], cats[:split]), (texts[split:], cats[split:])


def training_nlp(epochs=10, limit=0, output_dir="tweet_analyze/nlp1"):
    """
    Train the neural network in order to get the best model possible

    Args:
        epochs (int): number of iterations
        limit (int): max number of tweets
        output_dir (str): location where the model will be saved

    Returns:
        None
    """

    # Builds pipeline
    nlp = spacy.load("en_core_web_sm")
    if "textcat" not in nlp.pipe_names:
        textcat = nlp.create_pipe("textcat")
        nlp.add_pipe(textcat, last=True)
    else:
        textcat = nlp.get_pipe('textcat')

    textcat.add_label('INSULTING')

    # Loading the data
    print("We are loading the data from the file!")
    (train_texts, train_cats), (dev_texts, dev_cats) = load_data(limit=limit)
    training_data = list(
        zip(train_texts, [{'cats': cats} for cats in train_cats]))

    # Training only textcat and not the other pipes
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'textcat']
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        print("Beginning of the training session...")
        print('{:^5}\t{:^5}\t{:^5}\t{:^5}'.format('Loss', 'P', 'R', 'F'))
        batch_sizes = compounding(4.0, 32.0, 1.001)
        for i in range(epochs):
            loss = {}
            random.shuffle(training_data)
            # Creation of the batches
            batches = minibatch(training_data, size=batch_sizes)
            for batch in batches:
                texts, insult = zip(*batch)
                # Training with the batch
                nlp.update(texts, insult, sgd=optimizer,
                           drop=0.2, losses=loss)

            # Shows the evaluation of the model at the end of an epoch
            with textcat.model.use_params(optimizer.averages):
                scores = evaluate(nlp.tokenizer, textcat, dev_texts, dev_cats)
            print('{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}'
                  .format(loss['textcat'], scores['precision'],
                          scores['recall'], scores['f_score']))

    # Saves the model
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()
    nlp.to_disk(output_dir)
    print("Saved model to", output_dir)


def test(dir="tweet_analyze/nlp1"):
    """
    Tests the model with a comment written by the user
    """
    text = input("Enter a text to test : ")
    nlp = spacy.load(dir)
    doc = nlp(text)
    print(text, doc.cats)


def evaluate(tokenizer, textcat, texts, cats):
    """ Evaluates the model and return different parmeters about success

    Args:
        tokenizer
        textcat : pipeline used
        texts(list) : texts for the test
        cats(bool list) : indicates if it's insulting or not

    Returns:
        dict : dictionnary with precision, recall and f-score
    """

    docs = (tokenizer(text) for text in texts)
    tp = 1e-8  # True positives
    fp = 1e-8  # False positives
    fn = 1e-8  # False negatives
    tn = 1e-8  # True negatives
    for i, doc in enumerate(textcat.pipe(docs)):
        gold = cats[i]
        for label, score in doc.cats.items():
            if label not in gold:
                continue
            if score >= 0.5 and gold[label] >= 0.5:
                tp += 1.
            elif score >= 0.5 and gold[label] < 0.5:
                fp += 1.
            elif score < 0.5 and gold[label] < 0.5:
                tn += 1
            elif score < 0.5 and gold[label] >= 0.5:
                fn += 1
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f_score = 2 * (precision * recall) / (precision + recall)
    return {'precision': precision, 'recall': recall, 'f_score': f_score}


# Main function to apply on the tweets
def analyse_nlp1(tweets):
    """
    Uses the current model to evaluate how toxic is a dataframe of tweets

    Args:
        tweets (dataframe): dataframe of tweets

    Returns:
        dataframe : New column with the evaluation made by the NLP in [0,1] where 0  means correct and 1 offensing
    """

    nlp = spacy.load("tweet_analyze/nlp1")
    nlp1_insult = []
    for text in tweets["text"]:
        doc = nlp(text)
        nlp1_insult.append(doc.cats['INSULTING'])
    tweets['nlp1_insult_estimation'] = nlp1_insult
    return tweets


if __name__ == "__main__":
    # You're a fucking bitch
    # print(load_data())
    # training_nlp(epochs=20)
    test()

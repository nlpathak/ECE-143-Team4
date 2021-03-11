import pandas as pd
import numpy as np
import pickle
import os

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression

import scipy.sparse

from nltk.tokenize import TweetTokenizer

from gensim.models import Word2Vec
import nltk
nltk.download('punkt')

# Use nltk custom TweetTokenizer for our task
tweetTokenizer = TweetTokenizer(strip_handles=True, preserve_case=False)

def train_classifier(train_df, test_df, vectorizer, stop_words=None, max_features=200000, ngram_range=(1,3), C=1.0):
    '''
    Train a LogisticRegression model via vectorized data that is done through CountVectorizer or TfidfVectorizer.
    Write the model and the data used out to files for use later. 

    :param train_df: dataframe holding the training data
    :type train_df: pandas dataframe
    :param test_df: dataframe holding the testing data
    :type test_df: pandas dataframe
    :param vectorizer: class type for the vectorizer used for the model data
    :type vectorizer: type
    :param stop_words: stop_words for the vectorizer to ignore
    :type stop_words: str
    :param max_features: number of features for our vectorizer to consider at max
    :type max_features: int
    :param ngram_range: range of the ngrams that can be features of the data
    :type ngram_range: tuple
    :param C: the inverse regularization strength of the LogisticRegression model
    :type: float 
    '''

    assert isinstance(train_df, pd.DataFrame) and isinstance(test_df, pd.DataFrame)
    assert vectorizer is CountVectorizer or vectorizer is TfidfVectorizer
    assert not stop_words or stop_words == 'english' # don't support any other stop words
    assert isinstance(max_features, int) and max_features > 0 
    assert isinstance(ngram_range, tuple) and len(ngram_range) == 2
    assert isinstance(ngram_range[0], int) and isinstance(ngram_range[1], int) and ngram_range[0] <= ngram_range[1]
    assert isinstance(C, float) and C > 0 

    vect = vectorizer(stop_words=stop_words, max_features=max_features, tokenizer=tweetTokenizer.tokenize, ngram_range=ngram_range)

    print('Vectorizing data...')
    # vectorize training and testing data
    X_train = vect.fit_transform([entry['text'] for i, entry in train_df.iterrows()])
    Y_train = np.array([int(entry['target']) for i, entry in train_df.iterrows()])

    X_test = vect.transform([entry['text'] for i, entry in test_df.iterrows()])
    Y_test = np.array([int(entry['target']) for i, entry in test_df.iterrows()])

    print('Training Model...')
    # train classifier
    model = LogisticRegression(C=C, max_iter=15000)
    model.fit(X_train, Y_train)

    # evaluate classifier
    print(f'\nLogisticRegression Classifier using {vectorizer.__name__}')
    print(f'Training Accuracy: {np.mean(model.predict(X_train) == Y_train)}')
    print(f'Testing Accuracy: {np.mean(model.predict(X_test) == Y_test)}')

    # instead of returning all these things, save the vectorizer, model, and data to files for external use
    name = 'count' if vectorizer is CountVectorizer else 'tfidf'

    os.makedirs('./out', exist_ok=True)    
    pickle.dump(vect, open(f'./out/{name}_vect.pickle', 'wb'))
    pickle.dump(model, open(f'./out/{name}_model.pickle', 'wb'))
    scipy.sparse.save_npz(f'./out/{name}_vect_X_train.npz', X_train)
    np.save(f'./out/{name}_vect_Y_train.npy', Y_train)
    scipy.sparse.save_npz(f'./out/{name}_vect_X_test.npz', X_test)
    np.save(f'./out/{name}_vect_Y_test.npy', Y_test)


def train_w2v(train_df):
    '''
    Train a Word2Vec model for generating similarity scores of words for visualization. 
    Write the model out to file for use later. 

    :param train_df: dataframe holding the training data
    :type train_df: pandas dataframe
    '''
    assert isinstance(train_df, pd.DataFrame) 

    tweets = [entry['text'].lower() for i, entry in train_df.iterrows()]
    words = [tweetTokenizer.tokenize(tweet) for tweet in tweets]

    w2v = Word2Vec(words, min_count=5)
    
    os.makedirs('./out', exist_ok=True)    
    w2v.save('./out/word2vec.model') # write to file


# Functions to analyze the models

def getExtremeWords(vectorizer, model):
    '''
    Returns most extreme positive and negative words/phrases learned by the model

    :param vectorizer: the trained vectorizer used for the model data
    :type vectorizer: CountVectorizer or TfidfVectorizer
    :param model: the trained LogisticRegression classifier
    :type model: LogisticRegression
    '''
    assert isinstance(vectorizer, (CountVectorizer,TfidfVectorizer))
    assert isinstance(model, LogisticRegression)
    feature_names = np.array(vectorizer.get_feature_names())
    order = np.argsort(model.coef_)
    
    # Top 50 Most Negative Words/Phrases in Order, Top 50 Most Positive Words/Phrases in Order    
    return feature_names[order[0, :50]], feature_names[order[0, -50:]][::-1] # negative, positive    


def predict(tweets, vectorizer, model):
    '''
    Returns the predictions and confidence of the predictions for each tweet given

    :param tweets: list of tweets to predict on
    :type tweets: list of str
    :param vectorizer: the trained vectorizer used for the model data
    :type vectorizer: CountVectorizer or TfidfVectorizer
    :param model: the trained LogisticRegression classifier
    :type model: LogisticRegression
    '''
    assert isinstance(vectorizer, (CountVectorizer,TfidfVectorizer))
    assert isinstance(model, LogisticRegression)
    assert isinstance(tweets, list) and all([isinstance(tweet, str) for tweet in tweets])

    tweet_vectors = vectorizer.transform(tweets)
    preds = model.predict_proba(tweet_vectors)
    returnList = []
    for i, tweet in enumerate(tweets):
        pred = "Negative" if np.argmax(preds[i]) == 0 else "Positive"
        returnList.append((tweet, pred, np.max(preds[i])))
    return returnList


def analyzeTweets(tweets, vectorizer, model):
    '''
    Returns per word connotations of a tweet

    :param tweets: list of tweets to analyze
    :type tweets: list of str
    :param vectorizer: the trained vectorizer used for the model data
    :type vectorizer: CountVectorizer or TfidfVectorizer
    :param model: the trained LogisticRegression classifier
    :type model: LogisticRegression
    '''
    assert isinstance(vectorizer, (CountVectorizer,TfidfVectorizer))
    assert isinstance(model, LogisticRegression)
    assert isinstance(tweets, list) and all([isinstance(tweet, str) for tweet in tweets])

    returnList = []
    for tweet in tweets:
        tweetList = []
        for word in tweetTokenizer.tokenize(tweet.lower()):
            word = word.lower()
            if word in vectorizer.get_feature_names():
                index = vectorizer.get_feature_names().index(word)
                tweetList.append((word, model.coef_[0, index]))
            else: # not a top feature
                tweetList.append((word, 0))
        returnList.append(tweetList)
    return returnList


def getMostSimilarWords(tweets, w2v_model):
    '''
    For each word in each tweet, return the most similar learned words to that word along with the similarity score

    :param tweets: list of tweets to analyze
    :type tweets: list of str
    :param w2v_model: the trained Word2Vec Model
    :type model: Word2Vec
    '''
    assert isinstance(tweets, list) and all([isinstance(tweet, str) for tweet in tweets])
    assert isinstance(w2v_model, Word2Vec)

    returnList = []
    for tweet in tweets:
        tweetList = []
        for word in tweetTokenizer.tokenize(tweet.lower()):
            if word in w2v_model.wv.vocab:
                tweetList.append((word, w2v_model.wv.most_similar(word)))
            else: # not seen enough by the word2vec model to make prediction
                tweetList.append((word, []))
        returnList.append(tweetList)
    return returnList
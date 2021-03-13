from wordcloud import WordCloud, STOPWORDS, get_single_color_func
import matplotlib.pyplot as plt 
import pandas as pd
import pickle
import get_users_with_bearer_token
import user_tweets
from collections import Counter
import numpy as np
from datetime import date
import model_functions as MF
import string
import time
from time import sleep
import nltk
import os

# import pickled data
TfIdf_Model = pickle.load(open('tfidf_model.pickle', 'rb'))
TfIdf_Vectorizer = pickle.load(open('tfidf_vect.pickle', 'rb'))

CountVect_Model = pickle.load(open('count_vect_model.pickle', 'rb'))
CountVect_Vect = pickle.load(open('count_vectorizer.pickle', 'rb'))




class ColorWC(object):
    '''
    Class colors words red or green in word map based on positive or negative rating.
    '''
    
    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (get_single_color_func(color), set(words))
            for (color, words) in color_to_words.items()]
        self.default_color_func = get_single_color_func(default_color)

    def get_color_func(self, word):
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func
        return color_func

    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)



while input("new search? (y/n): ") == 'y':
    username = input("Input twitter username: ")
    userDat = get_users_with_bearer_token.main(username)
    
    while input('Username found: ' + userDat['data'][0]['name'] + '. Proceed with search? (y/n): ') != 'y':
        userDat = get_users_with_bearer_token.main(username)
    tweetCount = 100
    
    if input('Select the model to use: Tf-Idf (1) or Count Vectorizer (2): ') == '1':
        model = TfIdf_Model
        vectorizer = TfIdf_Vectorizer
        modelLabel = 'Tf-Idf'
    else:
        model = CountVect_Model
        vectorizer = CountVect_Vect
        modelLabel = 'Count Vectorizer'
    print('Retrieving 100 of the most recent tweets of user: ', userDat['data'][0]['name'], '...')
    
    userTweets, tweetDates = user_tweets.main(userDat['data'][0]['id'], tweetCount)
    # strip punctuation
    userTweets = [''.join(c for c in s if c not in string.punctuation) for s in userTweets]
    tweetWords = [word for line in userTweets for word in line.split()]
    wordCounter = Counter({})
    wordCounter = wordCounter + Counter(tweetWords)
    tweetObj = MF.predict(userTweets, vectorizer, model, silence=True)
    
    stopwords = set(STOPWORDS) 
    redlist = []
    greenlist = []
    
    # count word frequency
    wordCounterDict1 = dict(wordCounter)
    wordCounterDict1 = dict(sorted(wordCounterDict1.items(), key=lambda item: item[1], reverse=True))
    listDict1 = list(wordCounterDict1.keys())
    wordCounterDict = wordCounterDict1
    listDict = list(wordCounterDict.keys())
    
    print('Parsing tweets to generate word cloud...')
    for i, word in enumerate(listDict):
        if wordCounterDict[word] < 2:
            wordCounterDict.pop(word, None)
        # twitter reads ampersands oddly so pop off amp
        if word == 'amp':
            wordCounterDict.pop(word, None)
        elif word in vectorizer.get_feature_names():
            index = vectorizer.get_feature_names().index(word)
            rating = model.coef_[0, index]
            # assign as green or red based on prediction
            if rating > 0:
                greenlist.append(word)
            else:
                redlist.append(word)           
        else: 
            rating = 0
            wordCounterDict.pop(word, None)




    wc = WordCloud(width = 800, height = 600, 
                        max_words = 50,
                        min_word_length = 3,
                        background_color = '#dcf0f7',
                        min_font_size = 12)
    wc.generate_from_frequencies(frequencies=wordCounterDict)

    color_to_words = {
        # postive words below will be colored green
        '#00ff00': greenlist,
        # negative  words will be colored red
        '#ff0000': redlist
    }

    # create word cloud with color mapping
    colorwc = ColorWC(color_to_words, '#CCC5C5')
    wc.recolor(color_func=colorwc)

    # plot word cloud
    plt.figure()
    plt.imshow(wc)
    plt.axis('off')
    name = str(userDat['data'][0]['name'])
    plt.title('Word Cloud of Most Used Words of ' + name +'\'s Twitter')
    plt.show()
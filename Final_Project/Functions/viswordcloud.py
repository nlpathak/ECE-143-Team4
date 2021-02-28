from wordcloud import WordCloud, STOPWORDS, get_single_color_func
import matplotlib.pyplot as plt 
import pandas as pd
import pickle
import gensim
import get_users_with_bearer_token
import user_tweets
from collections import Counter
import numpy as np
from datetime import date
import ModelFunctions as MF
import string
import time


TfIdf_Model = pickle.load(open('tfidf_model.pickle', 'rb'))
TfIdf_Vectorizer = pickle.load(open('tfidf_vect.pickle', 'rb'))
w2v = gensim.models.Word2Vec.load('word2vec.model')

CountVect_Model = pickle.load(open('count_vect_model.pickle', 'rb'))
CountVect_Vect = pickle.load(open('count_vectorizer.pickle', 'rb'))


##########################################################################################


class ColorWC(object):
    '''
    gives red or green coloring to colors in word map based on positive or negative rating
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


##########################################################################################


while input("new search? (y/n): ") == 'y':
    username = input("Input twitter username: ")
    userDat = get_users_with_bearer_token.main(username)
    
    while input('Username found: ' + userDat['data'][0]['name'] + '. Proceed with search? (y/n): ') != 'y':
        username = input("Input twitter username: ")
        userDat = get_users_with_bearer_token.main(username)
    tweetCount = int(input("Input quantity of most recent tweets to analyze (100-3,200 in 100 intervals): "))
    assert isinstance(tweetCount, int) and 100 <= tweetCount <= 3200
    
    if input('Select the model to use: Tf-Idf (1) or Count Vectorizer (2): ') == '1':
        model = TfIdf_Model
        vectorizer = TfIdf_Vectorizer
        modelLabel = 'Tf-Idf'
    else:
        model = CountVect_Model
        vectorizer = CountVect_Vect
        modelLabel = 'Count Vectorizer'
    print('Retrieving up to ', tweetCount, ' of the most recent tweets of user: ', userDat['data'][0]['name'], '...')
    
    userTweets, tweetDates = user_tweets.main(userDat['data'][0]['id'], tweetCount)
    userTweets = [''.join(c for c in s if c not in string.punctuation) for s in userTweets]
    tweetWords = [word for line in userTweets for word in line.split()]
    wordCounter = Counter({})
    wordCounter = wordCounter + Counter(tweetWords)
    tweetObj = MF.predict(userTweets, vectorizer, model, silence=True)
    
    stopwords = set(STOPWORDS) 
    wordCounterDict = dict(wordCounter)
    listDict = list(wordCounterDict.keys())  
    # start_time = time.time()
    redlist = []
    greenlist = []
    
    for i, word in enumerate(listDict):
        if wordCounterDict[word] < 2 or word == 'amp':
            wordCounterDict.pop(word, None)
        elif word in vectorizer.get_feature_names():
            index = vectorizer.get_feature_names().index(word)
            rating = model.coef_[0, index]
            if rating > 0:
                greenlist.append(word)
            else:
                redlist.append(word)           
        else: 
            rating = 0
            wordCounterDict.pop(word, None)
            
    #print("--- %s seconds ---" % (time.time() - start_time))

    wc = WordCloud(width = 1200, height = 800, 
                        max_words = 100,
                        min_word_length = 3,
                        min_font_size = 10)
    wc.generate_from_frequencies(frequencies=wordCounterDict)

    color_to_words = {
        # postive words below will be colored green
        'green': greenlist,
        # negative  words will be colored red
        'red': redlist
    }

    # create word cloud with color mapping
    colorwc = ColorWC(color_to_words, 'grey')
    wc.recolor(color_func=colorwc)

    # plot word cloud
    plt.figure()
    plt.imshow(wc)
    plt.axis('off')
    name = str(userDat['data'][0]['name'])
    plt.title('Word Cloud of Most Used Words of ' + name +'\'s Twitter')
    plt.show()
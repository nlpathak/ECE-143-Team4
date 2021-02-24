import get_users_with_bearer_token
import user_tweets
import pickle
import gensim
import ModelFunctions as MF
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

#Load trained models
TfIdf_Model = pickle.load(open('tfidf_model.pickle', 'rb'))
TfIdf_Vectorizer = pickle.load(open('tfidf_vect.pickle', 'rb'))
w2v = gensim.models.Word2Vec.load('word2vec.model')
CountVect_Model = pickle.load(open('count_vect_model.pickle', 'rb'))
CountVect_Vect = pickle.load(open('count_vectorizer.pickle', 'rb'))


print('Tweet checker. Test the positivity of your tweet (before sending it!)')

userText = input('Type your tweet to check or \'end\' if you\'re done')
while userText != 'end':

    userText = input('Type your tweet to check or \'end\' if you\'re done')
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

print('Chronological tweets analysis, by user')
while input("new search? (y/n): ") == 'y':
    #Data Collection
    username = input("Input twitter username: ")
    tweetCount = int(input("Input quantity of most recent tweets to analyze (qty to within 100's increment, max 3,200): "))
    userDat = get_users_with_bearer_token.main(username)
    userTweets, tweetDates = user_tweets.main(userDat['data'][0]['id'], tweetCount)
    tweetObj = MF.predict(userTweets, CountVect_Vect, CountVect_Model, silence=True)
    tweetDict = {'tweets':userTweets, 'tweetDates':tweetDates, 'prediction': [predict for x, predict, y in tweetObj], 'confidence': [conf for x, y, conf in tweetObj]}
    start = date(int(tweetDict['tweetDates'][-1][0:4]), int(tweetDict['tweetDates'][-1][5:7]), int(tweetDict['tweetDates'][-1][8:10]))
    end = date(int(tweetDict['tweetDates'][0][0:4]), int(tweetDict['tweetDates'][0][5:7]), int(tweetDict['tweetDates'][0][8:10]))

    #Processing Data
    #daywiseTweets stores the quantity of tweets in a day aswell as the net quantity of positive/negative tweets
    daywiseTweets = np.zeros((2,(end - start).days))
    for tweetIdx in range(len(tweetDict['tweetDates'])):
        tweetDate = date(int(tweetDict['tweetDates'][tweetIdx][0:4]), int(tweetDict['tweetDates'][tweetIdx][5:7]),
                   int(tweetDict['tweetDates'][tweetIdx][8:10]))
        daywiseTweets[0][(tweetDate-start).days-1] += 1
        daywiseTweets[1][(tweetDate-start).days-1] += 1 if tweetDict['prediction'][tweetIdx] == 'Positive' else -1

    #processing on daywiseTweets for data visualization
    extrema = np.maximum(np.max(daywiseTweets[1]),np.abs(np.min(daywiseTweets[1])))
    daywiseTweets[1] = daywiseTweets[1] + extrema
    daywiseTweets[1] = daywiseTweets[1]/(2*extrema)

    #plotting data
    cmap = cm.get_cmap('RdYlGn')
    with plt.style.context('dark_background'):
        plt.bar(range(len(daywiseTweets[0])), daywiseTweets[0], color=cmap(daywiseTweets[1]))
        plt.title('Chronological ordering and positivity indication of ' + userDat['data'][0]['name'] + '\'s tweets')
        plt.xlabel('days from ' + str(start))
        plt.ylabel('tweet quantity by day')
    plt.show()



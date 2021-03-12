import get_users_with_bearer_token
import user_tweets
import pickle
import model_functions as MF
from datetime import date, timedelta
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import matplotlib.dates as mdates
import os

'''
With proper bearer token authentication, chronological_tweets performs a search on a twitter username, pulling
a specified quantity of tweets and does classification of positive or negative with the use of a NLP model.
The data and classifications are visualized by a chronologically ordered graph representing the quantity of tweets
and a color gradient of the quantity of positive and negative tweets, all per day as represented by a bar. 
'''


#Load trained models

TfIdf_Model = pickle.load(open('tfidf_model.pickle', 'rb'))
TfIdf_Vectorizer = pickle.load(open('tfidf_vect.pickle', 'rb'))

#w2v = gensim.models.Word2Vec.load('word2vec.model')
CountVect_Model = pickle.load(open('count_vect_model.pickle', 'rb'))
CountVect_Vect = pickle.load(open('count_vectorizer.pickle', 'rb'))

print('Chronological tweets analysis, by user')
bearerToken = input('Please input bearer token: ')
assert isinstance(bearerToken, str)
assert 150 > len(bearerToken) > 50, "Not a valid bearer token"
os.environ["BEARER_TOKEN"] = bearerToken

while input("new search? (y/n): ") == 'y':
    #Data Collection
    username = input("Input twitter username: ")
    assert 15 >= len(username) >= 4, "This is not a valid username. Length between 15 and 4 characters."
    userDat = get_users_with_bearer_token.main(username)
    while input('Username found: ' + userDat['data'][0]['name'] + '. Proceed with search? (y/n): ') != 'y':
        username = input("Input twitter username: ")
        assert 15 >= len(username) >= 4, "This is not a valid username. Length between 15 and 4 characters."
        userDat = get_users_with_bearer_token.main(username)
    tweetCount = int(input("Input quantity of most recent tweets to analyze (100-3,200 in 100 intervals): "))
    assert isinstance(tweetCount, int) and 100 <= tweetCount <= 3200, "Tweet count must be an int between 3,200 and 100"

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
    assert len(userTweets[0])>1, 'No data pulled. :('
    tweetObj = MF.predict(userTweets, vectorizer, model, silence=True)
    tweetDict = {'tweets':userTweets, 'tweetDates':tweetDates, 'prediction': [predict for x, predict, y in tweetObj], 'confidence': [conf for x, y, conf in tweetObj]}
    start = date(int(tweetDict['tweetDates'][-1][0:4]), int(tweetDict['tweetDates'][-1][5:7]), int(tweetDict['tweetDates'][-1][8:10]))
    end = date(int(tweetDict['tweetDates'][0][0:4]), int(tweetDict['tweetDates'][0][5:7]), int(tweetDict['tweetDates'][0][8:10]))

    #Processing Data
    #daywiseTweets stores the quantity of tweets in a day aswell as the net quantity of positive/negative tweets
    daywiseTweets = np.zeros((2,(end - start).days + 1))

    #mostPos/Neg stores the index of the day aswell as the day object and tweets that occured in that day and most pos/neg tweet overall
    mostPos = [[0],[], [], [0], [0]]
    mostNeg = [[0],[], [], [0], [0]]
    for tweetIdx in range(len(tweetDict['tweetDates'])):
        tweetDate = date(int(tweetDict['tweetDates'][tweetIdx][0:4]), int(tweetDict['tweetDates'][tweetIdx][5:7]),
                   int(tweetDict['tweetDates'][tweetIdx][8:10]))
        daywiseTweets[0][(tweetDate-start).days-1] += int(1)
        daywiseTweets[1][(tweetDate-start).days-1] += 1 if tweetDict['prediction'][tweetIdx] == 'Positive' else -1
        if daywiseTweets[1][(tweetDate-start).days-1] > mostPos[0]:
            mostPos[0] = daywiseTweets[1][(tweetDate-start).days-1]
            mostPos[1] = tweetDate
        if tweetDict['confidence'][tweetIdx] > mostPos[4] and tweetDict['prediction'][tweetIdx] == 'Positive':
            mostPos[3] = tweetIdx
            mostPos[4] = tweetDict['confidence'][tweetIdx]
        if daywiseTweets[1][(tweetDate-start).days-1] < mostNeg[0]:
            mostNeg[0] = daywiseTweets[1][(tweetDate-start).days-1]
            mostNeg[1] = tweetDate
        if tweetDict['confidence'][tweetIdx] > mostNeg[4] and tweetDict['prediction'][tweetIdx] == 'Negative':
            mostNeg[3] = tweetIdx
            mostNeg[4] = tweetDict['confidence'][tweetIdx]

    # processing on daywiseTweets for data visualization
    extrema = np.maximum(np.max(daywiseTweets[1]), np.abs(np.min(daywiseTweets[1])))
    daywiseTweets[1] = daywiseTweets[1] + extrema
    daywiseTweets[1] = daywiseTweets[1] / (2 * extrema)

    for tIdx, tDate in enumerate(tweetDates):
        if int(tDate[0:4]) == mostPos[1].year and int(tDate[5:7]) == mostPos[1].month and int(tDate[8:10]) == mostPos[
            1].day:
            mostPos[2].append(userTweets[tIdx])
        if int(tDate[0:4]) == mostNeg[1].year and int(tDate[5:7]) == mostNeg[1].month and int(tDate[8:10]) == mostNeg[
            1].day:
            mostNeg[2].append(userTweets[tIdx])

    # Most Positive Day/ tweet
    print('-------------------------------------------------------------')
    print('Showing all tweets on most positive day, ', str(mostPos[1]), ': \n')
    for tIdx in range(len(mostPos[2])):
        print(mostPos[2][tIdx])
    print('\nThe most positive tweet: \n')
    print(userTweets[mostPos[3]])
    print('-------------------------------------------------------------\n')

    # Most Negative Day/ tweet
    print('-------------------------------------------------------------')
    print('Showing all tweets on most negative day, ', str(mostNeg[1]), ': \n')
    for tIdx in range(len(mostNeg[2])):
        print(mostNeg[2][tIdx])
    print('\nThe most negative tweet: \n')
    print(userTweets[mostNeg[3]])
    print('-------------------------------------------------------------')

    #plotting data
    cmap = cm.get_cmap('RdYlGn')
    with plt.style.context('dark_background'):
        days = mdates.drange(start, end + timedelta(days=1), timedelta(days=1))
        plt.bar(days, daywiseTweets[0], color=cmap(daywiseTweets[1]))
        if len(days) <10:
            intervalDaysAxis = 2
            maf_width = int(len(daywiseTweets[0]) / 2)
        elif 50 > len(days)>= 10:
            intervalDaysAxis = int(len(days)/5)
            maf_width = int(len(daywiseTweets[0]) / 5)
        else:
            intervalDaysAxis = int(len(days)/15)
            maf_width = int(len(daywiseTweets[0]) / 15)
        smoothed = np.convolve(daywiseTweets[0], np.ones(maf_width)/maf_width)
        smoothed = smoothed[0:len(daywiseTweets[0]-1)]
        plt.plot(days, smoothed, '--', color='cyan', linewidth=5.5)
        plt.title(userDat['data'][0]['name'] + ', tweets/day: ' + '{:.2f}'.format(np.average(daywiseTweets[0])), fontsize=40)
        # plt.xlabel('days from ' + str(start) + ', Model used: ' + modelLabel + ', Span: ' + str(start) + ' - ' + str(end), fontsize=30)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=intervalDaysAxis))
        plt.gcf().autofmt_xdate()
        plt.ylabel('tweet count', fontsize=25)
    plt.show()

print('Thank you for using Chronological Tweet analyzer')

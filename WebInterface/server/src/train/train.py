import numpy as np
import pickle
from django.conf import settings 
import gensim

class SentimentAnalyzer:
    """
    Uses the tfidf model to predict sentiment on user tweets.
    """
    def __init__(self):
        self.pickle_root = settings.PICKLE_ROOT[0]
        print(self.pickle_root)
        with open(self.pickle_root + '/tfidf_vect.pickle', 'rb') as f:
            self.read_vect = pickle.load(f)
        with open(self.pickle_root + '/tfidf_model.pickle', 'rb') as f:
            self.read_model = pickle.load(f)

    def getExtremeWords(self):
        '''
        Returns top 50 negative and positive words.
        '''
        feature_names = np.array(self.read_vect.get_feature_names())
        order = np.argsort(self.read_model.coef_)

        top_neg = feature_names[order[0, :50]]
        top_pos = feature_names[order[0, -50:]][::-1]

        extreme = {'top_neg':top_neg,'top_pos':top_pos}
        return extreme

    def predict(self, tweets):
        tweet_vectors = self.read_vect.transform(tweets)
        predictions = self.read_model.predict_proba(tweet_vectors)
        sentiment = list(map(lambda x: "Negative" if np.argmax(x) == 0 else "Positive", predictions))
        confidence = list(map(lambda x: np.max(x), predictions))
        returnList = list(zip(tweets,sentiment,confidence))

        return returnList

    def analyzeTweets(self, tweets):
        """
        Analyzes tweets and returns a list of ...
        :param tweets:
        :param self.read_vect:
        :param model:
        :return : list of lists of tuples
        """
        assert isinstance(tweets, list)
        assert all([isinstance(x,str) for x in tweets])
        returnList = []
        for tweet in tweets:
            tweetList = []
            for word in tweet.split():
                word = word.lower()
                if word in self.read_vect.get_feature_names():
                    index = self.read_vect.get_feature_names().index(word)
                    print(f'Word: {word}, Connotation: {self.read_model.coef_[0, index]:.3f}')
                    tweetList.append((word, self.read_model.coef_[0, index]))
                else: # not a top feature
                    print(f'Word: {word}, Connotation: {0:.3f}')
                    tweetList.append((word, 0))
        returnList.append(tweetList)
        print()
        return returnList

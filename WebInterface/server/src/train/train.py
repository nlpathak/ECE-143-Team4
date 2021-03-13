import numpy as np
import pickle
from django.conf import settings 
import gensim
from nltk.tokenize import TweetTokenizer
import nltk


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
        Returns most extreme positive and negative words/phrases learned by the model

        :param vectorizer: the trained vectorizer used for the model data
        :type vectorizer: CountVectorizer or TfidfVectorizer
        :param model: the trained LogisticRegression classifier
        :type model: LogisticRegression
        '''
        feature_names = np.array(self.read_vect.get_feature_names())
        order = np.argsort(self.read_model.coef_)

        top_neg = feature_names[order[0, :50]]
        top_pos = feature_names[order[0, -50:]][::-1]

        extreme = {'top_neg':top_neg,'top_pos':top_pos}
        return extreme

    def predict(self, tweets):
        '''
        Returns the predictions and confidence of the predictions for each tweet given
        :param tweets: list of tweets to predict on
        :type tweets: list of str
        '''
        assert isinstance(tweets, list) and all([isinstance(tweet, str) for tweet in tweets])
        tweet_vectors = self.read_vect.transform(tweets)
        predictions = self.read_model.predict_proba(tweet_vectors)
        sentiment = list(map(lambda x: "Negative" if np.argmax(x) == 0 else "Positive", predictions))
        confidence = list(map(lambda x: np.max(x), predictions))
        returnList = list(zip(tweets,sentiment,confidence))

        return returnList

    def analyzeTweets(self, tweets):
        """
        Returns per word connotations of a tweet.
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
                    tweetList.append((word, self.read_model.coef_[0, index]))
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
        nltk.download('punkt')
        returnList = []
        for tweet in tweets:
            tweetList = []
            for word in tweetTokenizer.tokenize(tweet.lower()):
                if word in w2v_model.wv.vocab:
                    tweetList.append((word, w2v_model.wv.most_similar(word)))
                else:
                    tweetList.append((word, []))
            returnList.append(tweetList)
        return returnList

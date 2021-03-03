from gensim.models import Word2Vec
import nltk
from nltk.tokenize import TweetTokenizer
from django.conf import settings

tweetTokenizer = TweetTokenizer(strip_handles=True, preserve_case=False)
nltk.download('punkt')

def getMostSimilarWords(tweet):

    w2v_model = Word2Vec.load(settings.PICKLE_ROOT[0]+'/word2vec.model')
    # returnList = []
    tk = tweetTokenizer.tokenize(tweet)
    retList = [(x,w2v_model.most_similar(x)) for x in tk if x in w2v_model.wv.vocab]
    return retList

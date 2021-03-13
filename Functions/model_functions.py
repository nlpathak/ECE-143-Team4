import numpy as np

def predict(tweets, vectorizer, model, silence=False):
    '''
    Returns the predictions and confidence of the predictions for each tweet given

    :param tweets: list of tweets to predict on
    :type tweets: list of str
    :param model: the trained LogisticRegression classifier
    :type model: LogisticRegression
    '''
    
    #tweets of type list
    tweet_vectors = vectorizer.transform(tweets)
    preds = model.predict_proba(tweet_vectors)
    returnList = []
    for i, tweet in enumerate(tweets):
        if not silence:
            print(f'Tweet: {tweet}')
        pred = "Negative" if np.argmax(preds[i]) == 0 else "Positive"
        if not silence:
            print(f'Prediction: {pred}')
            print(f'Confidence of {pred} Prediction (0 to 1): {np.max(preds[i])}')
            print()
        returnList.append((tweet, pred, np.max(preds[i])))
    return returnList

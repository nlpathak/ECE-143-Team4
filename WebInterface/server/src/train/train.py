def getExtremeWords(vectorizer, model):
    feature_names = np.array(read_vect.get_feature_names())
    order = np.argsort(read_model.coef_)

    print("Top 50 Most Negative Words/Phrases in Order:")
    print(feature_names[order[0, :50]])
    print()
    print("Top 50 Most Positive Words/Phrases in Order:")
    print(feature_names[order[0, -50:]][::-1])

    return feature_names[order[0, :50]], feature_names[order[0, -50:]][::-1] # negative, positive    

def predict(tweets, vectorizer, model):
    tweet_vectors = vectorizer.transform(tweets)
    preds = model.predict_proba(tweet_vectors)
    returnList = []
    for i, tweet in enumerate(tweets):
        print(f'Tweet: {tweet}')
        pred = "Negative" if np.argmax(preds[i]) == 0 else "Positive"
        print(f'Prediction: {pred}')
        print(f'Confidence of {pred} Prediction (0 to 1): {np.max(preds[i])}')
        print()
        returnList.append((tweet, pred, np.max(preds[i])))
    return returnList

def analyzeTweets(tweets, vectorizer, model):
    returnList = []
    for tweet in tweets:
        tweetList = []
        for word in tweet.split():
            word = word.lower()
            if word in vectorizer.get_feature_names():
                index = vectorizer.get_feature_names().index(word)
                print(f'Word: {word}, Connotation: {model.coef_[0, index]:.3f}')
                tweetList.append((word, model.coef_[0, index]))
            else: # not a top feature
                print(f'Word: {word}, Connotation: {0:.3f}')
                tweetList.append((word, 0))
    returnList.append(tweetList)
    print()
    return returnList

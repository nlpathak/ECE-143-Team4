import get_users_with_bearer_token
import user_tweets
import pickle

classifier = pickle.load(open('tfidf_model.pickle', 'rb'))
vectorizer = pickle.load(open('tfidf_vect.pickle', 'rb'))

while input('New search? (y/n): ') == 'y':
    #get_tweets_with_bearer_token.main()
    username = input("Input twitter username: ")
    userDat = get_users_with_bearer_token.main(username)
    userTweets = user_tweets.main(userDat['data'][0]['id'])

    print('\n----- Last 10 tweets by: ' + username + ' -----\n')
    for i in range(len(userTweets['data'])):
        print('"' + userTweets['data'][i]['text'] + '"')
        print('Classification: Positive' if classifier.predict(vectorizer.transform([userTweets['data'][i]['text']])) else 'Classification: Negative')
        print('\n')

exit
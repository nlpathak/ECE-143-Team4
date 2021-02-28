from django.shortcuts import render
from .models import TwitterUser, UserTweet
from .twitget import TwitGet
from django.http import HttpResponse
from train.train import SentimentAnalyzer

import os
import json

try:
    if 'BEARER_TOKEN' in os.environ:
        BEARER_T = os.environ['BEARER_TOKEN']
    else:
        print('BEARER_TOKEN NOT FOUND')
except EnvironmentError as e:
    print(e)



def user(request, user):
    """
    """
    assert isinstance(user,str) and len(user) > 0, "Invalid user."

    tweety = TwitGet() # Will not work without bearer token
    json_response = []
    try:
        # Attempt to get existing username
        json_response = tweety.get_user(user)
        if json_response:
            user_data = json_response['data'][0]
            # print(f'user data: {user_data}')
            user_data['profile_img'] = user_data.pop('profile_image_url')
            user_data.update({'profile_img':user_data['profile_img'].replace('_normal','')})
            if user_data['url']:
                user_data['profile_url'] = user_data.pop('url')
            else:
                del user_data['url']
                user_data['profile_url'] = f'https://twitter.com/{user}'
            user_data.update(user_data.pop('public_metrics'))
            new_user = TwitterUser(**user_data)
            new_user.save()
        else:
            return HttpResponse(f'User: {user} not found')

    except Exception as e:
        return HttpResponse(f"Exception thrown: {e}")

    # Get tweets if already queried, returns empty list if no match
    # if not tweets:
    try:
        analyzer = SentimentAnalyzer()
        tweets = tweety.get_tweets(new_user.id,10) # list of dicts containing tweets    
        if tweets:
            tweets_txt = [x['text'] for x in tweets] # get list of tweets
            predict = analyzer.predict(tweets_txt) # returns list of tuples i.e. (text,sentiment,confidence)
            [x.update({'sentiment':y[1],'confidence':y[2],'user':new_user}) for (x,y) in list(zip(tweets,predict))]
            for tweet in tweets:
                twt_obj = UserTweet(**tweet)
                twt_obj.save()
            
    except Exception as e:
        return HttpResponse(f'Tweet Exception: {e}')

    tweets = UserTweet.objects.filter(user=new_user)

    return render(request, 'user.html', context={'user':new_user, 'tweets':tweets})
    
    return HttpResponse(f"Request: {json_response['data']}. You're at the user index.")

def users(request):
    all_users = TwitterUser.objects.all()
    return render(request, 'users.html', {'users':all_users})


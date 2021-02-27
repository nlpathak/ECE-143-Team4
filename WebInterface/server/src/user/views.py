from django.shortcuts import render
from .models import TwitterUser, UserTweet
from .twitget import TwitGet
from django.http import HttpResponse

import os

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
    json_response = {}
    try:
        # Attempt to get existing username
        print(user)
        new_user = TwitterUser.objects.get(username=user)

    except TwitterUser.DoesNotExist:
        json_response = tweety.get_user(user)
        user_data = json_response['data'][0]
        new_user = TwitterUser(**user_data)
        new_user.save()

    except Exception as e:
        return HttpResponse(f"Exception thrown: {e}")

    try: 
        tweets = UserTweet.objects.filter(user=new_user)
    except:
        for tweet in tweety.get_tweets(new_user.id,10):    
            tweet.update({'user':new_user})
            tw_obj = UserTweet(**tweet)
            tw_obj.save()


    return render(request, 'user.html', context={'user':new_user, 'tweets':tweets})
    
    return HttpResponse(f"Request: {json_response['data']}. You're at the user index.")

def users(request):
    all_users = TwitterUser.objects.all()
    return render(request, 'users.html', {'users':all_users})


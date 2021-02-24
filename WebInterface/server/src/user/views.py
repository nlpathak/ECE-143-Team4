from django.shortcuts import render
from .models import TwitterUser
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
        json_response = tweety.connect_to_endpoint(user)
        user_data = json_response['data'][0]
        new_user = TwitterUser.objects.get(pk=user_data['id'])

    except TwitterUser.DoesNotExist:
        new_user = TwitterUser(**user_data)
        new_user.save()

    except Exception as e:
        return HttpResponse(f"Exception thrown: {e}")
        
    return render(request, 'user.html', context={'user':new_user})
    
    return HttpResponse(f"Request: {json_response['data']}. You're at the user index.")

def users(request):
    all_users = TwitterUser.objects.all()
    return render(request, 'users.html', {'users':all_users})


from django.shortcuts import render
from user.models import UserTweet
# Create your views here.
from django.http import HttpResponse
import random

def tweets(request):
    all_tweets = list(UserTweet.objects.all())
    random.shuffle(all_tweets)
    return render(request, "tweets.html", context={'tweets':all_tweets}) 

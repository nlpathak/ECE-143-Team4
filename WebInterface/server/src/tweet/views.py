from django.shortcuts import render
from user.models import UserTweet
# Create your views here.
from django.http import HttpResponse

def tweets(request):
    all_tweets = UserTweet.objects.all()
    return render(request, "tweets.html", context={'tweets':all_tweets}) 

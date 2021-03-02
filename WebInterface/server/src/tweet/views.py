from django.shortcuts import render
from user.models import UserTweet
from django.http import HttpResponse
from .utils import download_csv
import random

def tweets(request):
    all_tweets = list(UserTweet.objects.all())
    random.shuffle(all_tweets)
    return render(request, "tweets.html", context={'tweets':all_tweets}) 


def export_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    data = download_csv(request, UserTweet.objects.all())
    response = HttpResponse(data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    return response

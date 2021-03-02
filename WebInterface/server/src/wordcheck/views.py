from django.shortcuts import render
from wordcheck.forms import WordCheckForm
from django.http import HttpResponse
from train.train import SentimentAnalyzer
import string

def check_words(request):
    """
    Gets response from user of text to check.
    """
    # If user giving us data
    if request.method == 'POST':
        form = WordCheckForm(request.POST)
        if form.is_valid():
            txt = form.clean_txt()
            # Remove punctuation
            txt = txt.translate(str.maketrans('','',string.punctuation))
            unq = list(set(txt.split(' ')))
            analyzer = SentimentAnalyzer()

            retList = analyzer.predict(unq)
            txt_dict = [{'word':x[0],'sentiment':x[1],'confidence':x[2]} for x in retList]
            # Renew form...
            form = WordCheckForm()
            # return HttpResponse(f'Request{txt_dict}.')

            return render(request, 'wordcheck.html', context={'wordform':form,'predicted':txt_dict})
        else:
            return HttpResponse(f'Invalid Request.')
    else:
        form = WordCheckForm()

    return render(request, 'wordcheck.html', context={'wordform':form})

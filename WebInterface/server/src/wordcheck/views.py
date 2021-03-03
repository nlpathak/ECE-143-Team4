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
            analyzer = SentimentAnalyzer()

            retList = analyzer.predict([txt])[0]
            txt_dict = {'txt':retList[0],'sentiment':retList[1],'confidence':retList[2]}
            # Renew form...
            form = WordCheckForm()
            # return HttpResponse(f'Request{retList}.')

            return render(request, 'wordcheck.html', context={'wordform':form,'predicted':txt_dict})
        else:
            return HttpResponse(f'Invalid Request.')
    else:
        form = WordCheckForm()

    return render(request, 'wordcheck.html', context={'wordform':form})

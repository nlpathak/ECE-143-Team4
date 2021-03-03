from django.shortcuts import render
from wordcheck.forms import WordCheckForm
from django.http import HttpResponse
from train.train import SentimentAnalyzer
from wordcheck.utils import getMostSimilarWords
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
            form = WordCheckForm()
            # return HttpResponse(f'Request{retList}.')

        else:
            return HttpResponse(f'Invalid Request.')
    else:
        form = WordCheckForm()
        txt_dict = None

    return render(request, 'wordcheck.html', context={'wordform':form,'predicted':txt_dict})

def compare_words(request):
    """
    word2vec comparison
    """
    # If user giving us data
    if request.method == 'POST':
        form = WordCheckForm(request.POST)
        if form.is_valid():
            txt = form.clean_txt()
            # Remove punctuation
            retList = getMostSimilarWords(txt)
            form = WordCheckForm()
            return HttpResponse(f'Request{retList}.')

        else:
            return HttpResponse(f'Invalid Request.')
    else:
        ret_list = None
        form = WordCheckForm()

    return render(request, 'compare.html', context={'wordform':form,'txt':ret_list})


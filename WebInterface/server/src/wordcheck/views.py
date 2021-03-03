from django.shortcuts import render
from wordcheck.forms import WordCheckForm
from django.http import HttpResponse
from train.train import SentimentAnalyzer
from wordcheck.utils import getMostSimilarWords
import itertools
import random
import numpy as np
from matplotlib import colors as mcolors
import string

colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
c = [x for x in colors.values() if isinstance(x,str)]

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
            txt = txt.translate(str.maketrans('','',string.punctuation))

            # Get most similar words -> [word, [(sim,conf)]]
            retList = getMostSimilarWords(txt)

            # Format for putting in network graph, i.e. data -> list of list pairs
            # nodes -> unique words and colors
            init_wrds = list(set(np.array([x[0] for x in retList]).flatten()))

            # Basically gets rid of the nesting and puts into pairs of words -> [[]]
            pairs = [list(zip(itertools.repeat(x[0]),[y[0] for y in x[1]if not any((y[0] == p for p in string.punctuation))])) for x in retList]
            pairs = list(itertools.chain(*pairs))
            pairs = [list(x) for x in pairs]

            random.shuffle(c)
            nodes = [{'id':x, 'color':y} for x,y in list(zip(init_wrds,c))]

            form = WordCheckForm()
            # return HttpResponse(f'Pairs: {pairs}, Nodes: {nodes}.')

        else:
            return HttpResponse(f'Invalid Request.')
    else:
        pairs = None
        nodes = None
        txt = None
        form = WordCheckForm()

    return render(request, 'compare.html', context={'wordform':form,'data':pairs, 'nodes':nodes, 'txt':txt})


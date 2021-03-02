from django.shortcuts import render
from wordcheck.forms import WordCheckForm

def check_words(request):
    """
    Gets response from user of text to check.
    """
    # If user giving us data
    if request.method == 'POST':
        form = WordCheckForm(request.POST)
        if form.is_valid():
            return HttpResponse('Text received!')
    else:
        form = WordCheckForm()

    return render(request, 'wordcheck.html', context={'form':form})

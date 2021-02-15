from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render
from home.forms import UserForm
from django.forms import ValidationError
from django.urls import reverse

def home(request):
    """
        Returns a rendered home page.
        :param request:
        :return :
    """
    form = None
    if request.method == 'GET':
        form = UserForm()
    elif request.method =='POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['username']
        return HttpResponsePermanentRedirect(f'/user/{user}')
    return render(request, 'home.html', context = {'form':form}) 

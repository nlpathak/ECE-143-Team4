from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render
from home.forms import UserForm
from django.forms import ValidationError
from django.urls import reverse
import user.views

def make_form(request):
    """
    Makes form for search input in navbar section.
    """
    from home.forms import UserForm
    form = None
    if request.method == 'GET':
        form = UserForm()
    elif request.method =='POST':
        form = UserForm(request.POST)
    return form

def home(request):
    """
        Returns a rendered home page.
        :param request:
        :return :
    """
    form = make_form(request)
    if form.is_valid():
        user = form.cleaned_data['username']
    if request.method == 'POST':
        return HttpResponsePermanentRedirect(f'/user/{user}')
    return render(request, 'home.html', context = {'form':form}) 

def users(request):
    return user.views.users(request)
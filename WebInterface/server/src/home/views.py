from django.http import HttpResponse
from django.shortcuts import render
from home.forms import UserForm

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
        form = request.form
    return render(request, 'home.html', context = {'form':form})

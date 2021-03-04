from django.http import HttpResponse, Http404
from django.shortcuts import render
from home.forms import UserForm

def home(request):
    """
        Returns a rendered home page.
        :param request:
        :return :
    """
    form = None
    try:
        if request.method == 'GET':
            form = UserForm()
        elif request.method =='POST':
            form = request.form
        return render(request, 'home.html', context = {'form':form})
    except Exception as e:
        return Http404(f'Error fetching home: {e}')

from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    """
        Returns a rendered home page.
        :param request:
        :return :
    """

    return render(request, 'home.html')

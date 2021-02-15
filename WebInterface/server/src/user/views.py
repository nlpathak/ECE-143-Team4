from django.shortcuts import render
from django.forms import ValidationError


# Create your views here.
from django.http import HttpResponse

def user(request, user):
    """
    """
    assert isinstance(user,str) and len(user) > 0, "Invalid user."
    return HttpResponse(f"Request: {user}. You're at the user index.")

def users(request):
    return HttpResponse(f"Request: {request}. You're at the user index.")


from django.urls import path

from . import views

urlpatterns = [
    path('', views.check_words,name='wordcheck'),
    path('compare', views.compare_words, name='compare'),
]

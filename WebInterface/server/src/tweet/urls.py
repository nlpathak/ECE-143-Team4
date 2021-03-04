from django.urls import path

from . import views

urlpatterns = [
    path('', views.tweets,name='tweets'),
    path('csv',views.export_csv,name='csv'),
]

from django.urls import path

from . import views

urlpatterns = [
    path('', views.users, name='users'),
    path('<user>', views.user, name='user')
]

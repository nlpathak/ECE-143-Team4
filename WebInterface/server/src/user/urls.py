from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.users, name='users'),
    path('<user>', views.user, name='user')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


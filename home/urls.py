from django.urls import path
from . import views
from django.views.generic.base import RedirectView

app_name = 'home'

urlpatterns = [
    path('', views.home , name='home'),
    path('favicon.ico', RedirectView.as_view(url='/media/favicon.ico')),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout')
]

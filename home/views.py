from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.


def home(request):
    return render(request, 'home/homepage.html')


class Login(LoginView):
    pass


class Logout(LogoutView):
    pass









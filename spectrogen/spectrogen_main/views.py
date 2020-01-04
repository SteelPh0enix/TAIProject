from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect


# Create your views here.

def index(request):
    return render(request, 'index.html')


def login_user(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = authenticate(request, username=username, password=password)
    print("User: {0}".format(user))
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/')
    return render(request, 'index.html', context={'login_failure': True})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
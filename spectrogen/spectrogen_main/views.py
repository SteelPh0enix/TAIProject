from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.

def index(request):
    return render(request, 'index.html', {'login_form': AuthenticationForm()})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'index.html', {'login_form': form})


def logout_user(request):
    logout(request)
    return redirect('/')


def register_user(request):
    pass

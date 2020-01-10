from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


# Create your views here.

def index_with_error(request, error_message):
    return render(request, 'index.html', {'login_form': AuthenticationForm(),
                                          'error_popup_message': error_message})

def index_with_info(request, info_message):
    return render(request, 'index.html', {'login_form': AuthenticationForm(),
                                          'info_popup_message': info_message})


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
    if request.user.is_authenticated:
        return index_with_error(request, 'You must log off before creating an account!')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("welp, done")
            return index_with_info(request, 'User registered successfully, you may now log in.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import JsonResponse, HttpResponse

from . import forms, spectrogen, models
# Create your views here.


def index_with_error(request, error_message):
    return index(request, {'error_popup_message': error_message})


def index_with_info(request, info_message):
    return index(request, {'info_popup_message': info_message})


def index(request, additional_context=None):
    list_of_spectrograms = models.Spectrogram.objects.all().order_by('-date_added')
    votes_data = []

    for spectrogram in list_of_spectrograms:
        vote_data = {}
        if request.user.is_authenticated:
            try:
                models.SpectrogramVote.objects.get(
                    spectrogram=spectrogram, user=request.user)
                vote_data['user_voted'] = True
            except models.SpectrogramVote.DoesNotExist:
                vote_data['user_voted'] = False

        vote_data['votes'] = models.SpectrogramVote.objects.filter(
            spectrogram=spectrogram).count()

        votes_data.append(vote_data)

    context = {'login_form': AuthenticationForm(
    ), 'spectrogram_data': zip(list_of_spectrograms, votes_data)}

    if additional_context is not None:
        context.update(dict(additional_context))

    return render(request, 'index.html', context=context)


def login_user(request):
    if request.user.is_authenticated:
        return index_with_error(request, 'You are already logged in!')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
        return index(request, {'login_form': form})
    else:
        return index(request)


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
            return index_with_info(request, 'User registered successfully, you may now log in.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def add_spectrogram(request):
    if not request.user.is_authenticated:
        return index_with_error(request, 'You must log in before adding spectrogram!')

    if request.method == 'POST':
        form = forms.SpectrogramForm(request.POST)
        if form.is_valid():
            spectrogram = form.save(commit=False)

            spectrogram.author = request.user

            if spectrogram.timeframe_start is None:
                spectrogram.timeframe_start = 0

            if spectrogram.timeframe_end is None:
                spectrogram.timeframe_end = -1

            try:
                spectrogram_bytes, filename = spectrogen.create_spectrogram_from_video(
                    spectrogram.video_url, spectrogram.timeframe_start, spectrogram.timeframe_end)
            except:
                return render(request, 'add_spectrogram.html', {'form': form, 'error_popup_message': 'There was an error while creating the spectrogram!'})

            if os.path.exists(settings.MEDIA_ROOT + '/spectrograms/' + filename):
                return render(request, 'add_spectrogram.html', {'form': form, 'error_popup_message': 'Spectrogram already exists!'})

            spectrogram.image_file.save(filename, ContentFile(
                spectrogram_bytes.read()), save=False)

            spectrogram.save()
            return index_with_info(request, 'Spectrogram addedd successfully!')
    else:
        form = forms.SpectrogramForm()
    return render(request, 'add_spectrogram.html', {'form': form})


def spectrogram_toggle_fav(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'reason': 'User is not logged in!'})

    try:
        spectrogram = models.Spectrogram.objects.get(id=id)
    except models.Spectrogram.DoesNotExist:
        return JsonResponse({'status': 'error', 'reason': 'Requested spectrogram does not exist!'})

    try:
        models.SpectrogramVote.objects.get(
            spectrogram=spectrogram, user=request.user).delete()
    except models.SpectrogramVote.DoesNotExist:
        models.SpectrogramVote(spectrogram=spectrogram,
                               user=request.user).save()

    return JsonResponse({'status': 'OK', 'reason': 'Vote changed successfully!'})

def get_spectrogram_votes(request, id):
    try:
        spectrogram = models.Spectrogram.objects.get(id=id)
    except models.Spectrogram.DoesNotExist:
        return HttpResponse(status=204)

    votes = models.SpectrogramVote.objects.filter(spectrogram=spectrogram).count()
    return JsonResponse({'id': id, 'votes': votes})
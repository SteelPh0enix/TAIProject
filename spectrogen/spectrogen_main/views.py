import os
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
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

    return JsonResponse({'status': 'OK'})

def get_spectrogram_votes(request, id):
    try:
        spectrogram = models.Spectrogram.objects.get(id=id)
    except models.Spectrogram.DoesNotExist:
        return HttpResponse(status=204)

    votes = models.SpectrogramVote.objects.filter(spectrogram=spectrogram).count()
    return JsonResponse({'id': id, 'votes': votes})

def edit_spectrogram(request, id):
    if not request.user.is_authenticated:
        return index_with_error(request, 'You have to log in in order to edit spectrograms.')

    try:
        spectrogram = models.Spectrogram.objects.get(id=id)
    except models.Spectrogram.DoesNotExist:
        return index_with_error(request, 'Spectrogram you want to edit does not exist!')

    # This should be done using permissions system, but i'll leave it like that for now
    if spectrogram.author != request.user and request.user.username != 'admin':
        return index_with_error(request, "You don't have permissions to edit this spectrogram!")

    if request.method == 'POST':
        pass
    else:
        return render(request, 'edit_spectrogram.html')

def view_user_profile(request):
    if not request.user.is_authenticated:
        return index_with_error(request, 'You have to log in to see your profile.')

    list_of_spectrograms = models.Spectrogram.objects.filter(author=request.user).order_by('-date_added')
    votes = list()

    for spectrogram in list_of_spectrograms:
        votes.append(models.SpectrogramVote.objects.filter(
            spectrogram=spectrogram).count())


    if request.method == 'POST':
        user_edit_form = PasswordChangeForm(request.user, request.POST)
        if user_edit_form.is_valid():
            user = user_edit_form.save()
            update_session_auth_hash(request, user)
    else:
        user_edit_form = PasswordChangeForm(request.user)

    return render(request, 'user_profile.html', {'spectrograms_data': zip(list_of_spectrograms, votes), 'user_edit_form': user_edit_form})

def delete_spectrogram(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'id': id, 'status': 'error', 'reason': 'You are not logged in!'})

    try:
        spectrogram = models.Spectrogram.objects.get(id=id)
    except models.Spectrogram.DoesNotExist:
        return JsonResponse({'id': id, 'status': 'error', 'reason': 'Spectrogram you want to remove does not exist!'})

    # This should be done using permissions system, but i'll leave it like that for now
    if spectrogram.author != request.user and request.user.username != 'admin':
        return JsonResponse({'id': id, 'status': 'error', 'reason': 'You are not permitted to delete this spectrogram!'})

    spectrogram.delete()
    return JsonResponse({'id': id, 'status': 'OK'})
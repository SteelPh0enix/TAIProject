from django import forms
from . import models

class SpectrogramForm(forms.ModelForm):

    timeframe_start = forms.IntegerField(required=False)
    timeframe_end = forms.IntegerField(required=False)

    class Meta:
        model = models.Spectrogram
        fields = ['title', 'video_url', 'timeframe_start', 'timeframe_end']

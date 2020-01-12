from django import forms
from . import models

class SpectrogramForm(forms.ModelForm):

    timeframe_start = forms.IntegerField(required=False, min_value=0)
    timeframe_end = forms.IntegerField(required=False, min_value=0)

    class Meta:
        model = models.Spectrogram
        fields = ['title', 'video_url', 'timeframe_start', 'timeframe_end']


from django import forms
from . import models

from spectrogen import get_video_metadata

class SpectrogramForm(forms.ModelForm):

    timeframe_start = forms.IntegerField(required=False, min_value=0)
    timeframe_end = forms.IntegerField(required=False, min_value=1024)

    class Meta:
        model = models.Spectrogram
        fields = ['title', 'video_url', 'timeframe_start', 'timeframe_end']

    def clean(self):
        cleaned_data = super().clean()
        time_min = cleaned_data.get('timeframe_start')
        time_max = cleaned_data.get('timeframe_end')


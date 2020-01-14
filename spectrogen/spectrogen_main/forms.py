from django import forms
from . import models

from .spectrogen import get_video_metadata

class SpectrogramForm(forms.ModelForm):
    timeframe_start = forms.IntegerField(required=False, min_value=0)
    timeframe_end = forms.IntegerField(required=False, min_value=1024)

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['timeframe_start'].label = 'Timeframe start (ms)'
        self.fields['timeframe_end'].label = 'Timeframe end (ms)'

    class Meta:
        model = models.Spectrogram
        fields = ['title', 'video_url', 'timeframe_start', 'timeframe_end']

    def clean(self):
        cleaned_data = super().clean()
        time_min = cleaned_data.get('timeframe_start')
        time_max = cleaned_data.get('timeframe_end')
        
        try:
            video_meta = get_video_metadata(cleaned_data.get('video_url'))
        except:
            raise forms.ValidationError("Couldn't download video metadata, are you sure you have entered correct URL?")
        
        duration_ms = video_meta.get('duration') * 1000

        if time_min is None or time_min < 0:
            time_min = 0

        if time_max is None:
            time_max = duration_ms

        if time_min > time_max:
            raise forms.ValidationError("End of timeframe must occur before the beginning!")
            
        if time_max - time_min <= 1024:
            raise forms.ValidationError("Timeframe period must be greater than 1024 milliseconds!")

        if time_max - time_min > 100000:
            raise forms.ValidationError("Timeframe period can't be longer than 100 seconds!")

        if time_max > duration_ms:
            raise forms.ValidationError("Timeframe can't be longer than video, nor outside of it! (video length: {0}ms)".format(duration_ms))
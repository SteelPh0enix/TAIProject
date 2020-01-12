from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.

class Spectrogram(models.Model):
    title = models.CharField(max_length=100)
    image_file_path = models.FilePathField(allow_files=True, allow_folders=False, default=settings.MEDIA_ROOT)
    video_url = models.URLField()
    timeframe_start = models.IntegerField(default=0)
    timeframe_end = models.IntegerField(default=-1)
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), models.CASCADE)

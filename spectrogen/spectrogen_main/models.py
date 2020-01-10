from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.

class Spectrogram(models.Model):
    title = models.CharField(max_length=100)
    image_filename = models.FilePathField(path=settings.SPECTROGRAMS_DIR)
    video_url = models.URLField()
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), models.CASCADE)

from django.db import models
from django.urls import reverse

# Create your models here.


class Album(models.Model):
    album_title = models.CharField(max_length=250)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()

    def get_absolute_url(self):
        return reverse('music:album_id', args=[self.pk])

    def __str__(self):
        return self.album_title + " - " + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('music:album_id', args=[self.album.pk])

    def __str__(self):
        return self.song_title + " - " + self.album.artist

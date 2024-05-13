from django.db import models


class Track(models.Model):
    track_id = models.CharField(max_length=50, primary_key=True)
    artist_id = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    duration = models.DurationField()
    release_date = models.DateField()
    is_explict = models.BooleanField(default=False)

    def __str__(self):
        return self.title
from django.db import models


class Track(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)
    image = models.URLField(null=True)
    download_url = models.URLField(null=True)

    # meta
    duration = models.DurationField()
    """ суммарная длительность всех треков """

    release_date = models.DateField()
    """ длительность трека """

    def __str__(self):
        return self.title
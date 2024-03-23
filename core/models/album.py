from django.db import models

from core.models.track import Track


class Album(Track):
    tracks = models.ManyToManyField('Track', related_name='albums')

    def __str__(self):
        return self.title
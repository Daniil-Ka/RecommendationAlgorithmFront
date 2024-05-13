import time
from typing import Any, Tuple, Type

from yandex_music import Client
from threading import Thread
from time import sleep
from ..music.models import Track
from datetime import datetime, timedelta
import os

from ..music.serializers import TrackSerializer
from ..recomendation_model import Model


class Wave:
    def __init__(self, user_id, genre, language, max_duration, is_explict):
        self.user_id = user_id

        self.genre = genre
        self.language = language
        self.max_duration = max_duration
        self.is_explict = is_explict

        self.client = Client(token=os.getenv("YANDEX_MUSIC_TOKEN")).init()

        self.next_dicts = []
        self.story = []
        self.generate_thread = Thread(target=self.__generate_playlist)
        self.generate_thread.start()

    def __generate_playlist(self):
        artists = Model.predict_artists(self.genre, self.language)
        dur = timedelta(milliseconds=self.max_duration)

        first = Track.objects.filter(genre=self.genre, language=self.language, is_explict=self.is_explict).first()
        self.next_dicts.append(self.get_dict_from_model(first))

        all = Track.objects.all()
        tracks_predicted = filter(
            lambda t:
            t.artist in artists and
            t.duration < dur and
            t.is_explict <= self.is_explict,
            all
        )
        c = 0
        for model in tracks_predicted:
            while len(self.next_dicts) > 10:
                time.sleep(1)
            self.next_dicts.append(self.get_dict_from_model(model))
            c += 1

        print('END PREDICTED ', c)
        other_tracks = filter(
            lambda t:
            t.artist not in artists and
            t.duration < dur and
            t.is_explict <= self.is_explict and
            t.genre == self.genre and
            (t.language == 'ru') == (self.language == 'ru'),
            all
        )

        c = 0
        for model in other_tracks:
            while len(self.next_dicts) > 10:
                time.sleep(1)
            self.next_dicts.append(self.get_dict_from_model(model))
            c += 1

        print('END OTHER ', c)

    def next(self):
        while len(self.next_dicts) == 0:
            time.sleep(0.5)

        d = self.next_dicts.pop(0)
        self.story.append(d)
        return d

    def get_dict_from_model(self, model):
        cover_200, cover_1000, download = self.get_urls_from_model(model)
        serializer = TrackSerializer(model)
        serialized_data = serializer.data
        serialized_data['cover_url_200'] = cover_200
        serialized_data['cover_url_1000'] = cover_1000
        serialized_data['download_url'] = download
        return serialized_data

    def get_urls_from_model(self, model: Track):
        track = self.client.tracks(model.track_id)[0]
        cover_200 = track.get_cover_url('200x200')
        cover_1000 = track.get_cover_url('1000x1000')
        download = track.get_download_info(get_direct_links=True)[0]['direct_link']
        return cover_200, cover_1000, download

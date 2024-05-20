import itertools
import sys
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
    def __init__(self, user_id, genres: list, languages: list, max_duration, is_explict):
        self.user_id = user_id

        self.genres = genres
        self.languages = languages
        self.max_duration = timedelta(milliseconds=max_duration)
        self.is_explict = [False]
        if is_explict:
            self.is_explict.append(is_explict)

        self.client = Client(token=os.getenv("YANDEX_MUSIC_TOKEN")).init()

        self.next_dicts = []
        self.story = []
        self.generate_thread = Thread(target=self.__generate_playlist)
        self.generate_thread.start()

    def __generate_playlist(self):
        first = Track.objects.filter(
            genre__in=self.genres,
            language__in=self.languages,
            is_explict__in=self.is_explict,
            duration__lt=self.max_duration,
        ).order_by('?').first()
        self.next_dicts.append(self.get_dict_from_model(first))

        artists = Model.predict_unpopular_artists(self.genres, self.languages, top_n=7)

        predicted_tracks = Track.objects.filter(
            artist__in=artists,
            is_explict__in=self.is_explict,
            duration__lt=self.max_duration
        )

        c = 0
        for model in predicted_tracks:
            while len(self.next_dicts) > 10:
                time.sleep(1)
            c += 1
            try:
                self.next_dicts.append(self.get_dict_from_model(model))
            except Exception as e:
                print(e)
                continue

        print('END PREDICTED ', c)

        other_tracks = Track.objects.filter(
            genre__in=self.genres,
            language__in=self.languages,
            is_explict__in=self.is_explict,
            duration__lt=self.max_duration
        ).order_by('?')
        c = 0
        for model in other_tracks:
            while len(self.next_dicts) > 10:
                time.sleep(1)
            try:
                self.next_dicts.append(self.get_dict_from_model(model))
            except:
                continue
            c += 1

        print('END OTHER ', c)

    def next(self):
        while len(self.next_dicts) == 0:
            time.sleep(0.1)

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

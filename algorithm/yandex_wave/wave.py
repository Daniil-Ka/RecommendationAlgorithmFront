from .moods import Mood
from yandex_music import Client
from .radio import Radio
from threading import Thread
from time import sleep
from ..music.models import Track
from datetime import datetime, timedelta
import os
class Wave:
    story_tracks_ids = []
    user_id = None
    client = None
    radio = None
    current_track = None
    next_tracks = []
    worker = None

    def __init__(self, user_id, mood: Mood):
        self.user_id = user_id
        self.client = Client(token=os.getenv("YANDEX_MUSIC_TOKEN")).init()
        self.radio = Radio(client=self.client)
        stations = self.client.rotor_stations_list()
        station = None
        for i in stations:
            if i.station.id.type == "mood" and i.station.id.tag == mood.value:
                station = i.station

        _station_id = f'{station.id.type}:{station.id.tag}'
        _station_from = station.id_for_from
        self.next_tracks.append(
            self.__get_track_model(
                self.radio.start_radio(_station_id, _station_from)
            )
        )
        self.worker = Thread(target=self.__append_next_tracks_worker)
        self.worker.start()

    def next_track(self) -> Track:
        while len(self.next_tracks) < 1:
            if self.worker == None:
                self.worker = Thread(target=self.__append_next_tracks_worker())
                self.worker.start()
            sleep(0.2)
            continue

        if self.current_track:
            self.story_tracks_ids.append(self.current_track.id)

        self.current_track = self.next_tracks.pop(0)
        return self.current_track

    def __append_next_tracks_worker(self):
        while True:
            if len(self.next_tracks) < 5:
                print("finding tracks")
                self.next_tracks.append(
                    self.__get_track_model(
                        self.radio.play_next()
                    )
                )
            else:
                sleep(1)
            print("tracks in list: ", len(self.next_tracks))

    def __get_track_model(self, track):
        return Track(
            id=track.track_id,
            title=track.title,
            artist=track.artists_name()[0],
            image=track.get_cover_url("1000x1000"),
            download_url=track.get_download_info(get_direct_links=True)[0]['direct_link'],
            duration=timedelta(milliseconds=track.duration_ms),
            release_date=datetime.fromisoformat(track.albums[0].release_date).date(),
        )


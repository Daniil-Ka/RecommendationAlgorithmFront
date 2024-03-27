from .moods import Mood
from yandex_music import Client
from .radio import Radio
import os
class Wave:
    story_ids = []
    user_id = None
    client = None
    radio = None
    current_track = None

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
        self.current_track = self.radio.start_radio(_station_id, _station_from)

    def next_track_url(self):
        if len(self.story_ids) == 0:
            self.story_ids.append(self.current_track.track_id)
            url = self.current_track.get_download_info(get_direct_links=True)[0]['direct_link']
            return url

        self.story_ids.append(self.current_track.track_id)
        self.current_track = self.radio.play_next()
        url = self.current_track.get_download_info(get_direct_links=True)[0]['direct_link']
        return url


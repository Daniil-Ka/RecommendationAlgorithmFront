import asyncio
import datetime
from pprint import pprint

from yandex_music import Client, ClientAsync
from yandex_music import Track, TrackShort

from radio import Radio

import csv

import os


def get_record(track: Track, client: Client):
    title = f"{track.artists[0].name} - {track.title}"
    print(title)
    artists = track.artists_name()
    duration = track.duration_ms
    is_explict = track.content_warning is not None
    year = track.albums[0].year
    genre = track.albums[0].genre
    artist_tracks_count = sum([len(artist.get_tracks(page_size=10**4)) for artist in track.artists])
    artist_albums_count = sum([len(artist.get_albums(page_size=10**2)) for artist in track.artists])
    artist_likes = sum([client.artists_brief_info(art.id).artist.likes_count for art in track.artists])
    album_likes = sum([client.albums(alb.id)[0].likes_count for alb in track.albums])
    ratings_all = [client.artists_brief_info(art.id).artist.ratings for art in track.artists]
    max_rating_month = max([i.month for i in ratings_all])
    max_rating_week = max([i.week for i in ratings_all])
    max_rating_day = max([i.day for i in ratings_all])

    min_rating_month = min([i.month for i in ratings_all])
    min_rating_week = min([i.week for i in ratings_all])
    min_rating_day = min([i.day for i in ratings_all])

    return [title,
            artists,
            duration,
            is_explict,
            year,
            genre,
            artist_tracks_count,
            artist_albums_count,
            artist_likes,
            album_likes,
            max_rating_month,
            max_rating_week,
            max_rating_day,
            min_rating_month,
            min_rating_week,
            min_rating_day,
            track.id]


def get_station_iterator(client, station):
    r = Radio(client)
    _station_id = f'{station.id.type}:{station.id.tag}'
    _station_from = station.id_for_from

    yield r.start_radio(_station_id, _station_from)
    count_fails = 0
    while True:
        try:
            yield r.play_next()
            count_fails = 0
        except:
            count_fails += 1
        if count_fails == 5:
            r = Radio(client)
            _station_id = f'{station.id.type}:{station.id.tag}'
            _station_from = station.id_for_from
            yield r.start_radio(_station_id, _station_from)
            count_fails = 0
            print("УПАЛО 5+ РАЗ")




def main():
    client = Client(token=os.getenv("TOKEN")).init()
    print(os.environ["TOKEN"])
    stations = client.rotor_stations_list()
    mood_stations = []
    for st in stations:
        if st.station.id.type == "mood":
            mood_stations.append(st.station)
            print(st.station.id)

    with open("test.csv", "w", encoding="utf-8") as out:
        writer = csv.writer(out, lineterminator="\n", delimiter=";")
        writer.writerow(["Название",
                         "Список артистов",
                         "Продолжительность",
                         "Наличие мата",
                         "Год",
                         "Жанр",
                         "Количество треков у артиста",
                         "Количество альбомов у артиста",
                         "Количество лайков артиста",
                         "Количество лайков альбома",
                         "Макс. позиция артиста в рейтинге за месяц",
                         "Макс. позиция артиста в рейтинге за неделю",
                         "Макс. позиция артиста в рейтинге за день",
                         "Мин. позиция артиста в рейтинге за месяц",
                         "Мин. позиция артиста в рейтинге за неделю",
                         "Мин. позиция артиста в рейтинге за день",
                         "ID трека",
                         "Настроение"])

        total_count = 0
        titles = set()
        for st in mood_stations: # 18 станций
            count = 50
            print(datetime.datetime.now())
            for track in get_station_iterator(client, st):
                try:
                    if f"{track.artists[0].name} - {track.title}" in titles:
                        continue
                    record = get_record(track, client)
                    record.append(st.id.tag)
                    writer.writerow(record)
                    titles.add(record[0])
                    count -= 1
                    total_count += 1
                except:
                    pass
                if count < 1:
                    break
                print(total_count)





if __name__ == '__main__':
    main()

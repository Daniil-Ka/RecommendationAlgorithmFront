import csv
import os

from django.http import JsonResponse, HttpResponse
import uuid

from yandex_music import Client

from .yandex_wave import wave, moods
from .music.models import Track
from .music.serializers import TrackSerializer

from datetime import timedelta, datetime

users_waves = {}


def next_track(request):
    token = request.COOKIES.get('user-token')
    is_token_exists = token is not None
    if not is_token_exists:
        token = uuid.uuid4()
    if token not in users_waves:
        users_waves[token] = wave.Wave(token, moods.Mood.Cool)
    id = users_waves[token].next_track_id()
    track = None
    try:
        track = Track.objects.get(id=id)
    except:
        track = get_track_model_by_id(id)
        track.save()

    serializer = TrackSerializer(instance=track)
    response = JsonResponse(serializer.data)
    if not is_token_exists:
        response.set_cookie('user-token', token)
    return response

def upload(request):
    client = Client(token=os.getenv("YANDEX_MUSIC_TOKEN")).init()
    with open("test.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        h = reader.__next__()
        headers = {head : ind for head, ind in zip(h, range(0, len(h)))}
        skip_counts = 0
        saved = 0
        for row in reader:
            try:
                track = get_track_model_by_id(row[headers['ID трека']], client)
                track.save()
                saved += 1
                print(saved)
            except Exception as e:
                print(e)
                skip_counts +=1
                print("Пропущено: ", skip_counts)


    return HttpResponse(f"saved: {saved}, skipped: {skip_counts}")


def get_track_model_by_id(id, client=None):
    if client is None:
        client = Client(token = os.getenv("YANDEX_MUSIC_TOKEN"))
    track_obj = client.tracks(id)[0]

    track = Track(
        id=track_obj.id,
        title=track_obj.title,
        artist=track_obj.artists_name()[0],
        image=track_obj.get_cover_url("1000x1000"),
        download_url=track_obj.get_download_info(get_direct_links=True)[0]['direct_link'],
        duration=timedelta(milliseconds=track_obj.duration_ms),
        release_date=datetime.fromisoformat(track_obj.albums[0].release_date).date(),
    )

    return track
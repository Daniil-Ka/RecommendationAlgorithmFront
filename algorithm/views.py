from django.shortcuts import render
import uuid
from .yandex_wave import wave, moods

users_waves = {}


def index(request):
    token = request.COOKIES.get('user-token')
    if token is None:
        token = uuid.uuid4()
    response = render(request, "alg_index.html", context={"text": token})
    response.set_cookie('user-token', token)
    return response


def next_track(request):
    token = request.COOKIES.get('user-token')
    if token is None:
        token = uuid.uuid4()
    if token not in users_waves:
        users_waves[token] = wave.Wave(token, moods.Mood.Cool)
    url = users_waves[token].next_track_url()
    response = render(request, "track2.html", context={"track": url})
    response.set_cookie('user-token', token)
    return response

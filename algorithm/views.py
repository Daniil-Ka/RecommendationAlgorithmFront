import uuid
from django.http import JsonResponse
from .music.serializers import TrackSerializer
from .yandex_wave import wave, moods

users_waves = {}


def next_track(request):
    token = request.COOKIES.get('user-token')
    is_token_exists = token is not None
    if not is_token_exists:
        token = uuid.uuid4()
    if token not in users_waves:
        users_waves[token] = wave.Wave(token, moods.Mood.Cool)
    track = users_waves[token].next_track()

    serializer = TrackSerializer(instance=track)
    response = JsonResponse(serializer.data)
    if not is_token_exists:
        response.set_cookie('user-token', token)
    return response

import asyncio
import csv
import datetime
import random

import uuid
from django.http import JsonResponse, HttpResponse
from .music.serializers import TrackSerializer
from .music.models import Track
from .yandex_wave import wave

from .recomendation_model.model import Model

users_waves = {}


def next_track(request):
    token = request.COOKIES.get('user-token')
    is_token_exists = token is not None
    if not is_token_exists:
        token = uuid.uuid4()
    if token not in users_waves:
        users_waves[token] = wave.Wave(token, 'pop', 'ru', 5*60*1000, True)

    next_dict = users_waves[token].next()
    response = JsonResponse(next_dict)
    if not is_token_exists:
        response.set_cookie('user-token', token)
    return response


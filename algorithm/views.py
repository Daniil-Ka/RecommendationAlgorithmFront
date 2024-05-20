import asyncio
import csv
import datetime
import itertools
import json
import random

import uuid
from pprint import pprint

from django.http import JsonResponse, HttpResponse
from rest_framework import status

from .music.serializers import TrackSerializer
from .music.models import Track
from .yandex_wave import wave

from .recomendation_model.model import Model

users_waves = {}


def next_track(request):
    token = request.COOKIES.get('user-token')
    is_token_exists = token is not None
    if not is_token_exists:
        return JsonResponse(status=402, data={'error': 'filters didnt applied'})

    next_dict = users_waves[token].next()
    response = JsonResponse(next_dict)
    return response


def apply_filters(request):
    token = request.COOKIES.get('user-token')
    is_token_exists = token is not None
    if not is_token_exists:
        token = uuid.uuid4()
    data = json.loads(request.body)
    pprint(data)
    filters = data.get('filters')
    genres = []
    languages = ['ru', 'en']
    is_explict = data.get('profanity')
    duration = 5 * 60 * 1000  #int(data.get('time'))
    for filter in filters:
        filter_type = filter.get('filter')
        if filter_type == 'Жанры':
            genres_dicts = filter.get('selected')
            for g in genres_dicts:
                genres += translate_genre[g.get('name')]

        elif filter_type == 'Язык':
            languages_dicts = filter.get('selected')
            languages_filter = [translate_lang[g.get('name')] for g in languages_dicts]
            if len(languages_filter) != 0:
                languages = languages_filter

    all_genres = set()
    if not genres:
        for li in translate_genre.values():
            all_genres.update(li)
        genres = list(all_genres)
    print(all_genres)

    print(genres)
    print(languages)
    users_waves[token] = wave.Wave(token, genres, languages, duration, is_explict)

    response = HttpResponse(status=status.HTTP_200_OK)
    response.set_cookie('user-token', token)
    return response


translate_lang = {
    'Русский': 'ru',
    'Иностранный': 'en'
}

translate_genre = {
    "блюз": ['blues'],
    "вокальная музыка": ['vocaljazz', 'vocal', 'smoothjazz'],
    "джаз": ['jazz', 'conjazz', 'vocaljazz'],
    "инструментальная музыка": [],
    "кантри": ['country', 'local-indie'],
    "классика": ['classical', 'classicalmasterpieces'],
    "этническая музыка": ['african', 'arabicpop', 'reggae'],
    "рок": ['israelirock', 'rock', 'rusrock', 'hardrock', 'folkrock'],
    "рэп": ['rap', 'foreignrap', 'rusrap'],
    "ска": ['ska'],
    "техно": ['newwave', 'prog', 'industrial', 'rnb', 'electronics', 'newage', 'modern', 'alternative', 'trance'],
    "панк": ['dnb', 'punk'],
    "фолк": ['folkgenre', 'foreignbard', 'folk', 'latinfolk', 'eurofolk', 'folkmetal', 'folkrock'],
    "хип-хоп": ['dance', 'triphopgenre'],
    "шансон": ['shanson'],
    "поп": ['pop', 'estrada', 'ruspop', 'disco']
}

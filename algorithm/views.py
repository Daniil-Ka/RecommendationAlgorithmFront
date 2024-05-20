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
    filters = data.get('filters')
    genres = []
    languages = ['ru', 'en']
    is_explict = data.get('profanity')
    duration = 100 * 60 * 60 * 1000
    try:
        duration = int(data.get('time')) * 1000
    except:
        pass

    for filter in filters:
        filter_type = filter.get('filter')
        if filter_type == 'Жанры':
            genres_dicts = filter.get('selected')
            for g in genres_dicts:
                genres += translate_genre[g.get('name')]

        elif filter_type == 'Язык':
            languages_dicts = filter.get('selected')
            languages_filter = [translate_lang[g.get('name')] for g in languages_dicts]
            if len(languages_filter) == 0 or len(languages_filter) == 2:
                languages = all_languages.copy()
            elif languages_filter[0] == 'ru':
                languages = ru_languages.copy()
            elif languages_filter[0] == 'en':
                languages = en_languages.copy()

    all_genres = set()
    if not genres:
        for li in translate_genre.values():
            all_genres.update(li)
        genres = list(all_genres)


    print(genres)
    print(languages)
    print(is_explict)
    print(duration)
    users_waves[token] = wave.Wave(token, genres, languages, duration, is_explict)

    response = HttpResponse(status=status.HTTP_200_OK)
    response.set_cookie('user-token', token)
    return response


all_languages = ['cy', 'he', 'fa', 'nl', 'ca', 'ko', 'en', 'sq', 'bg', 'fr', 'pt', 'zh-cn', 'mk', 'fi', 'es', 'ja', 'no', 'id', 'sl', 'de', 'tl', 'hr', 'it', 'ro', 'so', 'th', 'hu', 'zh-tw', 'cs', 'af', 'el', 'sv', 'uk', 'ar', 'pl', 'vi', 'ru', 'sw']

en_languages = all_languages.copy()
en_languages.remove('ru')

ru_languages = ['ru']


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
    "рок": ['rock', 'rusrock', 'hardrock', 'folkrock'],
    "рэп": ['rap', 'foreignrap', 'rusrap'],
    "ска": ['ska'],
    "техно": ['newwave', 'prog', 'industrial', 'rnb', 'electronics', 'newage', 'modern', 'alternative', 'trance'],
    "панк": ['dnb', 'punk'],
    "фолк": ['folkgenre', 'foreignbard', 'folk', 'latinfolk', 'eurofolk', 'folkmetal', 'folkrock'],
    "хип-хоп": ['dance', 'triphopgenre'],
    "шансон": ['shanson'],
    "поп": ['pop', 'estrada', 'ruspop', 'disco']
}

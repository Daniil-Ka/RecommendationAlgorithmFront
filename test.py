import asyncio
import csv
import datetime
import os
import random

from yandex_music import ClientAsync

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django
django.setup()
from algorithm.music.models import Track

def load_database():
    models = asyncio.run(get_models('340k.csv'))
    print(len(models))
    Track.objects.bulk_create(models)
    print('succes')

async def get_models(filename):
    cors = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        headers_arr = reader.__next__()
        headers = dict()
        for i in range(0, len(headers_arr)):
            headers[headers_arr[i]] = i
        print(headers_arr)

        for row in reader:
            cors.append(get_model_from_row(row, headers))
        print(len(cors))

    models = [i for i in await asyncio.gather(*cors) if i]
    return models

async def get_model_from_row(row, headers):
    try:
        track_model = Track(
            track_id=row[headers['ID трека']],
            artist_id=row[headers['ID артиста']],
            title=row[headers['Название']],
            artist=row[headers['Артист']],
            genre=row[headers['Жанр']],
            language=row[headers['Язык']],
            duration=datetime.timedelta(milliseconds=int(row[headers['Продолжительность(мс)']])),
            release_date=datetime.datetime.fromisoformat(row[headers['Дата релиза']]),
            is_explict=row[headers['Наличие мата']] == 'True'
        )
        return track_model
    except Exception as e:
        return None



#load_database()
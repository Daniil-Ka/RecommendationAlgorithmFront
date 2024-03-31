import json
from django.shortcuts import render


def index(request):
    context = {
        'data': 'a',  # Передайте данные в шаблон
    }

    # Верните ответ с использованием шаблона и контекста
    return render(request, 'index.html', context)


def filter(request):
    titles = ["Жанры", "Язык", "Настроение", "На кого похоже"]

    genres = [
        "блюз", "вокальная музыка", "гранж", "джаз", "инструментальная музыка", "кантри", "классика",
        "этническая музыка", "рок", "ска", "техно", "панк", "фолк", "хип-хоп", "шансон"
    ]
    moods = [
        "aggressive", "spring", "sad", "winter", "beautiful", "cool",
        "summer", "dream", "haunting", "dark", "newyear", "autumn",
        "happy", "relaxed", "sentimental", "calm", "energetic", "epic"
    ]
    lang = ['Русский', 'Английский']

    filters = [genres, lang, moods, ['123']]

    context = {
        'titles': titles,
        'filters': json.dumps(filters)
    }

    return render(request, 'fitler.html', context)

import json
from typing import List, Tuple, Dict

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView


def generate_filters() -> dict:
    """ Создать заголовки и значения для фильтров """

    titles = ["Жанры", "Язык"]

    genres = [
        "блюз", "вокальная музыка", "гранж", "джаз", "инструментальная музыка", "кантри", "классика",
        "этническая музыка", "рок", "ска", "техно", "панк", "фолк", "хип-хоп", "шансон"
    ]
    moods = [
        "aggressive", "spring", "sad", "winter", "beautiful", "cool",
        "summer", "dream", "haunting", "dark", "newyear", "autumn",
        "happy", "relaxed", "sentimental", "calm", "energetic", "epic"
    ]

    filters = [genres, moods]

    context = {
        'titles': titles,
        'filters': json.dumps(filters)
    }

    return context

def index(request):
    context = generate_filters()
    # Верните ответ с использованием шаблона и контекста
    return render(request, 'index.html', context)


# фильтры
class BaseFilterView(APIView):
    def filter(self, query: str) -> List[Tuple[int, str]]:
        """ Вернуть отфильтрованные значения {"id": id, "name": name} """

    def get(self, request):
        query = request.GET.get('q', '')
        filtered_genres = self.filter(query)
        return Response(filtered_genres)


class GenreFilterView(BaseFilterView):
    def filter(self, query: str) -> List[Dict]:
        genres = [
            "блюз", "вокальная музыка", "джаз", "инструментальная музыка", "кантри", "классика",
            "этническая музыка", "рок", "ска", "техно", "панк", "фолк", "хип-хоп", "шансон", "рэп", 'поп'
        ]

        return [{'id': i, 'name': element} for i, element in enumerate(genres) if query.lower() in element.lower()]


class LangFilterView(BaseFilterView):
    def filter(self, query: str) -> List[Dict]:
        languages = [
            'Русский', 'Иностранный'
        ]

        return [{'id': i, 'name': element} for i, element in enumerate(languages) if query.lower() in element.lower()]

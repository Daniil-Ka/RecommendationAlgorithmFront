from django.shortcuts import render


def index(request):
    context = {
        'data': 'a',  # Передайте данные в шаблон
    }

    # Верните ответ с использованием шаблона и контекста
    return render(request, 'index.html', context)


def filter(request):
    context = {
        'data': 'a',  # Передайте данные в шаблон
    }
    return render(request, 'fitler.html', context)
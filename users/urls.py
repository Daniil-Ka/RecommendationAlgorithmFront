from django.urls import path

from users import views

urlpatterns = [
    path('', views.index),

    # автодополнение для фильтров
    path('filters/genre/', views.GenreFilterView.as_view()),
    path('filters/lang/', views.LangFilterView.as_view()),
    path('filters/mood/', views.MoodFilterView.as_view()),
    path('filters/similar/', views.SimilarFilterView.as_view()),

]
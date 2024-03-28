from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('next/', views.next_track)
]
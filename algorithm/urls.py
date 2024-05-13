from django.urls import path

from . import views

urlpatterns = [
    path('next/', views.next_track),
]
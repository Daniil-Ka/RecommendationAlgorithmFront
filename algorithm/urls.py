from django.urls import path

from . import views

urlpatterns = [
    path('next/', views.next_track),
    path('apply_filters/', views.apply_filters),
]

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

import users

urlpatterns = [
    path('admin/', admin.site.urls),
    path('algorithm/', include("algorithm.urls")),
    path('users/', include("users.urls")),

    path('for_musicians/', users.views.ForMusiciansView.as_view()),
    path('about/', users.views.AboutView.as_view()),
    path('docs/', users.views.DocsView.as_view()),

    path('', RedirectView.as_view(url='/users/', permanent=True))
]

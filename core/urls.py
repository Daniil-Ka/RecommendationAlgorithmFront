from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('algorithm/', include("algorithm.urls")),
    path('users/', include("users.urls"))
]

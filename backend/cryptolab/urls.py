"""
URL configuration for Classic CryptoLab project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/ciphers/', include('ciphers.urls')),
    path('api/attacks/', include('attacks.urls')),
    path('api/exercises/', include('exercises.urls')),
    path('api/messaging/', include('messaging.urls')),
]

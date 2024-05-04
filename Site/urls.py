from django.contrib import admin
from django.urls import path, include
from . import views
from FavArch import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Main),
    path('Libary', views.Libary),
    path('Error', views.Error)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
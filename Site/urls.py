from django.contrib import admin
from django.urls import path, include
from . import views
from FavArch import settings
from django.conf.urls.static import static
from .models import *

urlpatterns = [
    path('', views.Main),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),

    path('Libary', views.Libary, name='Libary'),
    path('Error', views.Error),
    path('about', views.about, name='about'),
    path('profile', views.Profile, name="profile"),
    path('bookAdd/<int:Book_id>/', views.BookAdd, name='book-add'),
    path('book-delete/<int:id>/', views.BookDelete, name='book-del'),
    path('download/<path:filename>/', views.download_file, name='download'),
    path('login', views.Login.as_view(), name="login"),
    path('register', views.register, name='register'),
    path('logout', views.logout, name="logout"),
    path('accounts/profile/', views.redirect_to_profile),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
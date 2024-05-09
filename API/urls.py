from django.urls import path
from .views import *

app_name = 'API'

urlpatterns = [
    path('books/', BooksView.as_view(), name='genres'),
]
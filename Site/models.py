import os
from datetime import timezone

from django.contrib.auth.models import User
from django.db import models
from django.http import HttpResponse

from FavArch import settings


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Book_img/')
    description = models.TextField(blank=True, default='Нет описания')
    book_file = models.FileField(upload_to='books/', blank=True)

    def __str__(self):
        return self.title

class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name='authors')

    def __str__(self):
        return self.last_name

class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserBookStatus(models.Model):
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.status

class UserBooks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.ForeignKey(UserBookStatus, on_delete=models.CASCADE, default=5)

    def __str__(self):
        return f'{self.book.title} для {self.user.username} | статус {self.status}'

class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    premiere = models.TextField()
    text = models.TextField()

    def __str__(self):
        return self.title
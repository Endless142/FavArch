from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Book_img/')
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.title

class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return self.last_name

class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
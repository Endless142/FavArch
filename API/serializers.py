from rest_framework import serializers
from Site.models import Book

class BooksSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=5000)


    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.last_name  # Получаем имя автора
        representation['genre'] = instance.genre.name  # Получаем имя жанра
        return representation
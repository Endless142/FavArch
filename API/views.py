from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from API.serializers import BooksSerializer
from Site.models import Book

# Create your views here.

class BooksView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        books = Book.objects.all()
        serializer = BooksSerializer(books, many=True)
        return Response({"books": serializer.data})


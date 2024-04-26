from django.shortcuts import render
from .models import Book
def Main(request):
    return render(request, 'Site/Главная.html')

def Libary(request):
    books = Book.objects.all()
    return render(request, 'Site/Библиотека.html', {'books': books})
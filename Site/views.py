import os
import zipfile
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .Forms import *
from django.contrib.auth import logout as logouts
from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,
)
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import Q

def Main(request):
    query = request.GET.get('q')  # Получение поискового запроса из GET-параметров

    if query:
        authors = User.objects.filter(username__startswith=query)
        author_ids = authors.values_list('id', flat=True)  # Получаем список id

        # Фильтруем статьи
        articles = Article.objects.filter(
            Q(title__icontains=query) |  # Поиск по названию
            Q(author_id__in=author_ids)  # Поиск по автору
        )
    else:
        articles = Article.objects.all()

    if request.method == 'POST':
        form = ArticleForm(request.POST, user=request.user)
        print('Форма:', form)  # Вывод данных формы
        if form.is_valid():
            print('Форма  валидна:', form.cleaned_data)
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = ArticleForm(user=request.user)
    context = {'articles': articles, 'form': form, 'query': query }
    return render(request, 'Site/Главная.html', context)

def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    context = {'article': article}
    return render(request, 'Site/article_detail.html', context)



def Libary(request):
    books = Book.objects.all()
    genre_id = request.GET.get('genre')
    if genre_id:
        books = books.filter(genre__id=genre_id)
    author_id = request.GET.get('author')
    if author_id:
        books = books.filter(author__id=author_id)
    context = {
        'books': books,        'genres': Genre.objects.all(),
        'authors': Author.objects.all()
    }
    return render(request, 'Site/Библиотека.html', context)

def Error(request):
    return render(request, 'Site/Error.html')

def Profile(request):
    if request.user.is_authenticated:
        context = {
            'prof': UserBooks.objects.filter(user=request.user),
            'fav': Favorite.objects.filter(user=request.user)
        }
    else:
        context = {
            'prof': UserBooks.objects.none(),
            'fav': Favorite.objects.none()
        }

    return render(request, 'Site/profile.html', context)


class Login(LoginView):
   template_name = 'Site/auth.html'
   form_class = AuthUserForm
   succces_url = ('/profile')


def get_success_url(self):
      return self.succces_url

def logout(request):
   if request.method == 'POST':
      logouts(request)
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def redirect_to_profile(request):
   return redirect('/profile')

def validate_password(password):
    """Валидация пароля."""
    validators = [
        UserAttributeSimilarityValidator,
        MinimumLengthValidator,
        CommonPasswordValidator,
        NumericPasswordValidator,
    ]

    for validator in validators:
        try:
            validator().validate(password)
        except ValidationError as e:
            raise ValidationError(e.messages)

    return True

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Проверка пароля перед сохранением
            try:
                user = form.save()
                return redirect("/profile")
            except ValidationError as e:
                # Вывод ошибок валидации пароля
                form.add_error("password", e.messages)
                # Отображение формы с ошибками
                return render(request, "Site/reg.html", {"form": form})

    else:
        form = RegistrationForm()

    return render(request, "Site/reg.html", {"form": form})

def BookAdd(request, Book_id):

   book = Book.objects.get(id=Book_id)
   userbook = UserBooks.objects.filter(user=request.user, book=book)

   if not userbook.exists():
      UserBooks.objects.create(user=request.user, book=book)
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   else:

      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def BookDelete(request, id):
   book = UserBooks.objects.get(id=id)
   book.delete()
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def download_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/x-fb2')
        # Измените Content-Disposition на inline
        response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
        return response


def about(request):
    return render(request, "Site/О-нас.html")

def FavAdd(request, fav_id):
   fav = Article.objects.get(id=fav_id)
   userfav = Favorite.objects.filter(user=request.user, article=fav)

   if not userfav.exists():
      Favorite.objects.create(user=request.user, article=fav)
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   else:

      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def FavDelete(request, id):
   fav = Favorite.objects.get(id=id)
   fav.delete()
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


from django.contrib import admin
from .models import *

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(UserBookStatus)
admin.site.register(UserBooks)
admin.site.register(Article)
admin.site.register(Favorite)
from django.contrib import admin

from .models import Movie, Theme, Comment

# Register your models here.

admin.site.register(Movie)
admin.site.register(Theme)
admin.site.register(Comment)

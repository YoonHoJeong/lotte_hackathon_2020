from django.contrib import admin

from .models import Theme, Movie, Comment, Vote

# Register your models here.
admin.site.register(Theme)
admin.site.register(Movie)
admin.site.register(Comment)
admin.site.register(Vote)

from django.contrib import admin

from .models import Theme, Movie, Comment, Vote, VoteMovie, Like

# Register your models here.
admin.site.register(Theme)
admin.site.register(Movie)
admin.site.register(VoteMovie)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(Like)

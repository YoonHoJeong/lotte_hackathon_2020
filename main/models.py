from django.db import models

# Create your models here.

class Theme(models.Model):
    #movie = models.ManyToManyField(Movie)
    title = models.CharField(max_length=200)

class Movie(models.Model):
    # 의견이 1개라도 작성된 Movie
    title = models.CharField(max_length=100)
    #theme = models.ManyToManyField(Theme)
    comment = models.PositiveIntegerField(blank = False)
    possible = models.BooleanField()
    subrun = models.BooleanField()
    
class Comment(models.Model):
    #movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
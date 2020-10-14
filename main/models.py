from django.db import models

# Create your models here.

class Movie(models.Model):
    # 의견이 1개라도 작성된 Movie
    title = models.CharField(max_length=100)

class Comment(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()

class Vote(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)


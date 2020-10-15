from django.db import models
from django.conf import settings

# Create your models here.


class Theme(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Movie(models.Model):
    # 의견이 1개라도 작성된 Movie를 저장
    title = models.CharField(max_length=100)
    theme = models.ManyToManyField(Theme)
    genre = models.CharField(max_length=200)
    director = models.CharField(max_length=200)
    production_year = models.PositiveIntegerField()
    runtime = models.PositiveIntegerField()
    plot = models.TextField()

    possible = models.BooleanField(default=False)    # 개봉 가능한지
    subrun = models.BooleanField(default=False)      # 이전에 개봉 했었는지

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

from django.db import models
from django.conf import settings

# Create your models here.


# 이번 달의 테마, 관리자가 생성함.
class Theme(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


# 의견이 1개라도 작성된 Movie를 저장
class Movie(models.Model):
    title = models.CharField(max_length=100)
    theme = models.ManyToManyField(Theme, default=None)

    genre = models.CharField(max_length=200)
    director = models.CharField(max_length=200)
    production_year = models.PositiveIntegerField()
    runtime = models.PositiveIntegerField()
    plot = models.TextField()

    movie_id = models.CharField(max_length=200)
    movie_seq = models.CharField(max_length=200)

    possible = models.BooleanField(default=False)    # 개봉 가능한지
    subrun = models.BooleanField(default=False)      # 이전에 개봉 했었는지

    def __str__(self):
        return self.title


# 투표 리스트에 올릴 영화 - 관리자가 등록할 영화들
class VoteMovie(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


# 의견글, 사용자, 영화, 생성된 시간이 기입됨.
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# 홈화면에서 투표, 투표수를 셀 때 사용.
class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

# 영화상세 화면에서 좋아요 수를 셀 때 사용.
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

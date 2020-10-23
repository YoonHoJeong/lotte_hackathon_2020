from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

import calendar
# Create your models here.


# 이번 달의 테마, 관리자가 생성함.
class Theme(models.Model):
    MONTH_CHOICES = [(str(i), calendar.month_name[i]) for i in range(1,13)]

    title = models.CharField(max_length=200)
    month = models.CharField(max_length=10, choices=MONTH_CHOICES, default='1')
    subtitle = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.title + " / " + f"{self.month}월"


# 의견이 1개라도 작성된 Movie를 저장
class Movie(models.Model):
    title = models.CharField(max_length=100)
    theme = models.ManyToManyField(Theme, default=None)
    poster = models.ImageField(blank=False, null=True)

    genre = models.CharField(max_length=200)
    director = models.CharField(max_length=200)
    production_year = models.PositiveIntegerField()
    runtime = models.PositiveIntegerField()
    plot = models.TextField()
    movie_id = models.CharField(max_length=200)
    movie_seq = models.CharField(max_length=200)

    possible = models.BooleanField(default=False)    # 개봉 가능한지
    subrun = models.BooleanField(default=False)      # 이전에 개봉 했었는
    
    num_like = models.PositiveIntegerField(default=0)

    @classmethod
    def create(cls, movie_obj):
        production_year = int(movie_obj.get('production_year') + '0')
        runtime = int(movie_obj.get('runtime') + '0')
        
        return cls(
            title= movie_obj.get('title'), 
            poster= movie_obj.get('poster'), 
            genre= movie_obj.get('genre'), 
            director= movie_obj.get('director'), 
            production_year= production_year,
            runtime= runtime,
            plot= movie_obj.get('plot'), 
            movie_id= movie_obj.get('movie_id'), 
            movie_seq= movie_obj.get('movie_seq')
        )


    def __str__(self):
        return self.title


# 투표 리스트에 올릴 영화 - 관리자가 등록할 영화들
class VoteMovie(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    vote_num = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return self.movie.title + " / " + self.theme.title


# 의견글, 사용자, 영화, 생성된 시간이 기입됨.
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " / " + self.movie.title

# 홈화면에서 투표, 투표수를 셀 때 사용.
class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " / " + self.movie.title

# 영화상세 화면에서 좋아요 수를 셀 때 사용.
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

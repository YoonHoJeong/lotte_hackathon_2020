from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from .models import Movie, Comment, Theme
from django.conf import settings
from datetime import datetime
from django.urls import reverse
from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required

import requests

from .models import VoteMovie, Vote, Movie, Comment, Like, Theme

API_KEY = "1YJNU2R902583045L4Z6"
BASE_URL = f"http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2&ServiceKey={API_KEY}"

# api 사용, 검색 결과 반환하는 함수
def get_search_list(queries):
    """ 
    검색 결과 내에 있는 영화들에서 필요한 정보만 추출
    1. title - 영화 제목
    2. poster - 영화 포스터, 없는 경우 많음.
    3. plot - 줄거리, 100자 까지만 보여주도록
    4. genre - 영화 장르, 쉼표(,)로 구분되어 있음.
    5. runtime - 상영 시간, 분 단위
    6. production_year - 제작년도
    7. director - 감독
    """

    search_list = []
    movie_list = []
    max_plot_length = 100
    query = ""

    for query_name, query_content in queries.items():
        query += f"&{query_name}={query_content}"

    res = requests.get(BASE_URL + query).json()

    # 검색 결과로 나온 영화 리스트
    movie_list = res['Data'][0].get('Result')

    search_cnt = res['TotalCount']  # 검색 결과 개수

    if not movie_list:  
        # 검색 결과가 없을 때
        return [], 0
    else:   
        # 검색 결과가 있을 때
        for movie in movie_list:
            tmp_movie = {}
            """ title parsing """
            title = movie['titleEtc']
            title_length = title.find("^")
            title = title[:title_length].strip()

            """ poster parsing """
            poster = movie['posters']
            poster_idx = poster.find("|")

            movie_id = movie['movieId']
            movie_seq = movie['movieSeq']
            
            """ plot contraction """
            plot = movie["plots"]['plot'][0]['plotText']
            if len(plot) > max_plot_length:
                plot = plot[:max_plot_length] + "..."

            if poster_idx != -1:
                poster = poster[:poster_idx]

            tmp_movie['title'] = title
            tmp_movie['plot'] = plot
            tmp_movie['genre'] = movie["genre"]
            tmp_movie['runtime'] = movie["runtime"]
            tmp_movie['poster'] = poster
            tmp_movie['production_year'] = movie['prodYear']
            tmp_movie['director'] = movie['directors']['director'][0]['directorNm']
            tmp_movie['movie_id'] = movie_id
            tmp_movie['movie_seq'] = movie_seq

            search_list.append(tmp_movie)
        return search_list, search_cnt

def isSavedMovie(movie, movie_id, movie_seq):
    return movie.movie_id == movie_id and movie.movie_seq == movie_seq

def get_month_theme(add_month):
    # 2달 뒤 테마
    certain_month = (int(datetime.now().strftime('%m')) + add_month) % 12
    if certain_month == 0:
        certain_month = 12

    # default theme - 다음 달
    theme = Theme.objects.filter(month = str(certain_month)).first()
    return theme
# Create your views here.

def home(request):
    # default theme - 다음 달
    theme = get_month_theme(1)

    votemovies = VoteMovie.objects.all()

    if theme != None :    
        votemovies = VoteMovie.objects.filter(theme__title=theme.title)
        votemovies = votemovies.order_by('-vote_num')

    return render(request, "home.html", {'votemovies' : votemovies, 'theme': theme})

def enroll_movie(request):
    themes = Theme.objects.all()
    comment_movies = Movie.objects.all()

    if not request.user.is_staff:
        return redirect("home")

    if request.method == "GET":
        return render(request, "enroll_movie.html", {'comment_movies':comment_movies, 'themes':themes})
    
    elif request.method == "POST":
        # '등록하기' 버튼을 눌렀을 때
        # vote_movie_instance = VoteMovie()
        movie_id = request.POST.get("movieId")
        movie_seq = request.POST.get("movieSeq")
        theme_id = request.POST.get("dropdown")

        movie = [movie for movie in comment_movies if isSavedMovie(movie, movie_id, movie_seq)]

        theme = get_object_or_404(Theme, id=theme_id)


        if movie:
            movie = movie[0]

            # 해당 영화가 Movie 리스트에 있으면 그대로 작성
            vote_movie = VoteMovie.objects.filter(theme__id=theme.id, movie__id = movie.id)

            if not vote_movie:
                # 이미 같은 테마의 영화가 vote_movie에 저장되어 있지 않을 때만
                
                vote_movie = VoteMovie()
                vote_movie.theme = theme
                vote_movie.movie = movie
                vote_movie.save()
            else:
                print("이미 같은 vote movie가 있어요")
        else:
            movie_obj = get_search_list({'movieId':movie_id, 'movieSeq':movie_seq})[0][0]
            movie = Movie.create(movie_obj)
            movie.save()

            vote_movie = VoteMovie()
            vote_movie.theme = theme
            vote_movie.movie = movie
            vote_movie.save()
            # movie.save()

        # 해당 영화가 Movie 리스트에 없으면 새로 Movie 생성
        # movie = get_search_list({"movieId":movie_id, "movieSeq":movie_seq})
    return redirect('enroll_movie')

def enroll_movie_search(request):
    search_list = []
    themes = Theme.objects.all()

    if request.method == "GET":
        comment_movies = Movie.objects.all()
        query = request.GET['query']

        if query:
            search_list, search_cnt = get_search_list({'title':query})
        else:
            return redirect('enroll_movie')

    return render(request, 'enroll_movie.html', {'comment_movies':comment_movies, 'search_list': search_list, 'themes':themes})

def comment(request):
    theme = get_month_theme(2) # 2달뒤 theme

    top_movies = Movie.objects.all().order_by('num_like')[:8]
    return render(request, "comment.html", {"top_movies" : top_movies, "theme": theme})

def movie_detail(request, movie_id = None):
    # vote movie처럼 기존 데이터가 있을 때
    if movie_id:
    
        movie = Movie.objects.get(pk= movie_id)
        if movie:
            comment_list = Comment.objects.filter(movie__id = movie_id)
            likes = Like.objects.filter(movie__id = movie_id)
            like_num = likes.count()
            user_like = likes.filter(user__id = request.user.id)
            print(like_num, user_like)
        return render(request, "movie.html", {"movie" : movie, "comment_list" : comment_list, "like_num" : like_num, 'user_like' : user_like})
    else:
        # POST 요청일 때, API 호출
        movie_id = request.POST.get("movieId")
        movie_seq = request.POST.get("movieSeq")
        movie = get_search_list({'movieId':movie_id, 'movieSeq':movie_seq})[0][0]
        if movie:
            return render(request, "movie.html", {"movie" : movie})
    return redirect("enroll_movie")


def movie(request):
    max_plot_length = 300    
    user_like = 0
    comment_list = []

    if request.method == "POST":
        movie_id = request.POST.get('movieId')
        movie_seq = request.POST.get('movieSeq')
        comment = request.POST.get('comment')

        movie_obj = Movie.objects.all() #현재 Movie model 전부 가져오기

        if movie_obj.filter(movie_id = movie_id, movie_seq=movie_seq).exists() == False : 
            # movie object가 있을 때
            res = requests.get(BASE_URL + f"&movieId={movie_id}&movieSeq={movie_seq}").json()

            result_list = res['Data'][0]['Result']

            for movie in result_list:

                tmp_obj = {}
                movie_title = movie['titleEtc']
                title_length = movie_title.find("^")
                movie_title = movie_title[:title_length].strip()
                poster = movie['posters']
                poster_idx = poster.find("|")

                plot = movie["plots"]['plot'][0]['plotText']
                if len(plot) > max_plot_length:
                    plot = plot[:max_plot_length] + "..."

                if poster_idx != -1:
                    poster = poster[:poster_idx]

                tmp_obj['title'] = movie_title
                tmp_obj['plot'] = plot
                tmp_obj['genre'] = movie["genre"]
                tmp_obj['runtime'] = movie["runtime"]
                tmp_obj['poster'] = poster
                tmp_obj['production_year'] = movie['prodYear']
                tmp_obj['director'] = movie['directors']['director'][0]['directorNm']
                tmp_obj['movie_id'] = movie_id
                tmp_obj['movie_seq'] = movie_seq

                break

            movie_instance = Movie(
                title = tmp_obj['title'], 
                genre =  tmp_obj['genre'],
                poster = tmp_obj['poster'],
                director = tmp_obj['director'], 
                production_year = tmp_obj['production_year'], 
                runtime = tmp_obj['runtime'], 
                plot = tmp_obj['plot'], 
                movie_id=movie_id, 
                movie_seq=movie_seq
            )

            movie_instance.save()
            # 모든 요소 가져와서 Movie 모델 생성

        selec_movie = movie_obj.filter(movie_id=movie_id, movie_seq=movie_seq)

        tmp_obj = selec_movie[0]        

        if comment :
            comment_instance = Comment(user = request.user, movie = tmp_obj, content = comment)        
            comment_instance.save()
        else :
            like_obj = Like.objects.all()

            user_like = 1

            if like_obj.filter(movie = tmp_obj, user = request.user).exists() == True :
                user_like = -1
 
            if user_like == 1:
                like_instance = Like(movie=tmp_obj, user=request.user)
                like_instance.save()      
                tmp_obj.num_like += 1

        comment_obj = Comment.objects.all()

        for comment in comment_obj :

            tmp_com_obj = {}

            if comment.movie.movie_seq == movie_seq and comment.movie.movie_id == movie_id :
                tmp_com_obj['created_at'] = comment.created_at
                tmp_com_obj['user'] = comment.user
                tmp_com_obj['content'] = comment.content

                comment_list.append(tmp_com_obj)            

    elif request.method == "GET":
        movie_id = request.GET.get('movieId')
        movie_seq = request.GET.get('movieSeq')

        comment_obj = Comment.objects.all()

        for comment in comment_obj :

            tmp_com_obj = {}

            if comment.movie.movie_seq == movie_seq and comment.movie.movie_id == movie_id :
                tmp_com_obj['created_at'] = comment.created_at
                tmp_com_obj['user'] = comment.user
                tmp_com_obj['content'] = comment.content

                comment_list.append(tmp_com_obj)

        res = requests.get(BASE_URL + f"&movieId={movie_id}&movieSeq={movie_seq}").json()

        result_list = res['Data'][0]['Result']

        for movie in result_list:

            tmp_obj = {}
            movie_title = movie['titleEtc']
            title_length = movie_title.find("^")
            movie_title = movie_title[:title_length].strip()
            poster = movie['posters']
            poster_idx = poster.find("|")

            plot = movie["plots"]['plot'][0]['plotText']
            
            if len(plot) > max_plot_length:
                plot = plot[:max_plot_length] + "..."

            if poster_idx != -1:
                poster = poster[:poster_idx]

            tmp_obj['title'] = movie_title
            tmp_obj['plot'] = plot
            tmp_obj['genre'] = movie["genre"]
            tmp_obj['runtime'] = movie["runtime"]

            tmp_obj['poster'] = poster
            tmp_obj['production_year'] = movie['prodYear']
            tmp_obj['director'] = movie['directors']['director'][0]['directorNm']
            tmp_obj['movie_id'] = movie_id
            tmp_obj['movie_seq'] = movie_seq

            break

    else:
        return redirect('comment')

    like_obj = Like.objects.all()

    like_num = 0

    for like in like_obj :
        if like.movie.movie_id == movie_id and like.movie.movie_seq == movie_seq :
            like_num += 1


    return render(request, "movie.html", {"movie" : tmp_obj, "comment_list" : comment_list, "like_num" : like_num, 'user_like' : user_like})

def search(request):
    # default theme - 다음 달
    theme = get_month_theme(2)

    # request -> response
    # response로 받은 데이터 뿌려주기
    query = ""
    search_list = []
    max_plot_length = 100

    if request.method == "GET":
        query = request.GET['query']
        if query:
            # 사용자가 검색어를 입력했을 때,
            search_list, search_cnt = get_search_list({'title':query})
            # 제목 단위로 검색.
        else:
            # 검색어가 없는 경우, api 호출 x
            return redirect('comment')

    return render(request, "search.html", {"search_list": search_list, "search_cnt": search_cnt, "theme":theme} )

@login_required(login_url='/login/')
def vote(request):
    theme = get_month_theme(1) # 다음달 테마
    votemovies = VoteMovie.objects.filter(theme__title = theme.title)

    if request.method == 'POST':

        vote_objs = Vote.objects.all()
        votemovie_id = request.POST.get('votemovie_id')
        vote_movie = VoteMovie.objects.get(pk=votemovie_id)

        movie_id = vote_movie.movie.id

        movie_obj = Movie.objects.get(pk=movie_id)

        is_already_vote = Vote.objects.filter(vote_movie = vote_movie, user = request.user)

        if is_already_vote:
            # 이미 투표했을 때
            return redirect("/?is_voted=1")
        else:
            # 투표를 안 했을 때
            vote = Vote()
            vote.user = request.user
            vote.vote_movie = vote_movie            
            vote_movie.vote_num = vote_movie.vote_num + 1
            vote.save()
            vote_movie.save()
            return redirect("/?is_voted=0")
    return redirect("home")

def unvote(request, vote_movie_id):
    vote = Vote.objects.filter(vote_movie__id = vote_movie_id, user__id = request.user.id).first()
    
    if vote:
        vote.delete()
        vote_movie = vote.vote_movie
        vote_movie.vote_num = len(vote_movie.get_voters())
        vote_movie.save()
        return redirect('/?unvote=True')
    return redirect('/?unvote=False')

def delete_vote_movie(request):
    if request.method == "POST":
        vote_movie_id = request.POST.get('votemovie_id')
        vmovie_instance = VoteMovie.objects.get(id=vote_movie_id)
        vmovie_instance.delete()

        return redirect("/?delete=1")
    return redirect("/?delete=0")
        


            





    
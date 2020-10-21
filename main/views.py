from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from .models import Movie, Comment, Theme
from django.conf import settings
from datetime import datetime

import requests

from .models import VoteMovie, Vote, Movie

API_KEY = "1YJNU2R902583045L4Z6"
BASE_URL = f"http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2&ServiceKey={API_KEY}"

# api 사용, 검색 결과 반환하는 함수
def get_search_list(query):
    search_list = []
    max_plot_length = 100

    res = requests.get(BASE_URL + f"&title={query}").json()

    # 검색 결과로 나온 영화 리스트
    result_list = res['Data'][0]['Result']
    search_cnt = res['TotalCount']  # 검색 결과 개수
    for movie in result_list:

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

        tmp_obj = {}
        title = movie['titleEtc']
        title_length = title.find("^")
        title = title[:title_length].strip()
        poster = movie['posters']
        poster_idx = poster.find("|")
        # idx = movie['DOCID']
        movie_id = movie['movieId']
        movie_seq = movie['movieSeq']
        
        plot = movie["plots"]['plot'][0]['plotText']
        if len(plot) > max_plot_length:
            plot = plot[:max_plot_length] + "..."

        if poster_idx != -1:
            poster = poster[:poster_idx]

        tmp_obj['title'] = title
        tmp_obj['plot'] = plot
        tmp_obj['genre'] = movie["genre"]
        tmp_obj['runtime'] = movie["runtime"]

        tmp_obj['poster'] = poster
        tmp_obj['production_year'] = movie['prodYear']
        tmp_obj['director'] = movie['directors']['director'][0]['directorNm']
        # tmp_obj['idx'] = idx 
        tmp_obj['movie_id'] = movie_id
        tmp_obj['movie_seq'] = movie_seq

        search_list.append(tmp_obj)
    return search_list, search_cnt


# Create your views here.

def home(request):
    votemovies = VoteMovie.objects.all()
    results = Vote.objects.values('movie_id').annotate(count=Count('movie_id'))
    total = Vote.objects.all().count()
    return render(request, "home.html", {'votemovies' : votemovies, 'results' : results})

def enroll_movie(request):
    themes = Theme.objects.all()

    if not request.user.is_staff:
        return redirect("home")

    if request.method == "GET":
        comment_movies = Movie.objects.all()

        return render(request, "enroll_movie.html", {'comment_movies':comment_movies, 'themes':themes})
    
    elif request.method == "POST":
        # '등록하기' 버튼을 눌렀을 때
        # vote_movie_instance = VoteMovie()
        print(request.POST.get("movieId"))
        print(request.POST.get("movieSeq"))

        # 해당 영화가 Movie 리스트에 있으면 그대로 작성

        # 해당 영화가 Movie 리스트에 없으면 새로 Movie 생성
    return redirect('enroll_movie')

def enroll_movie_search(request):
    search_list = []

    if request.method == "GET":
        comment_movies = Movie.objects.all()
        query = request.GET['query']
        print(request)
        if query:
            print(query)    
            search_list, search_cnt = get_search_list(query)
        else:
            return redirect('enroll_movie')

    return render(request, 'enroll_movie.html', {'comment_movies':comment_movies, 'search_list': search_list})

def comment(request):
    movies = Movie.objects.all()
    top_movies = Movie.objects.all().order_by('?')[:8]
    return render(request, "comment.html", {'movies' : movies, "top_movies" : top_movies})

def movie(request):

    max_plot_length = 300
    
    comment_list = []

    if request.method == "POST":
        movie_id = request.POST.get('movieId')
        movie_seq = request.POST.get('movieSeq')
        comment = request.POST.get('comment')

        movie_obj = Movie.objects.all() #현재 Movie model 전부 가져오기

        if movie_obj.filter(movie_id = movie_id, movie_seq=movie_seq).exists() == False : 

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

    return render(request, "movie.html", {"movie" : tmp_obj, "comment_list" : comment_list})


def search(request):
    # request -> response
    # response로 받은 데이터 뿌려주기
    query = ""
    search_list = []
    max_plot_length = 100

    if request.method == "GET":
        query = request.GET['query']
        if query:
            # 사용자가 검색어를 입력했을 때,
            search_list, search_cnt = get_search_list(query)
            # 제목 단위로 검색.
        else:
            # 검색어가 없는 경우, api 호출 x
            return redirect('comment')

    return render(request, "search.html", {"search_list": search_list, "search_cnt": search_cnt})


def vote(request):
    if request.method == 'POST':
        vote = Vote()
        vote.user_id = request.user.id
        vote.movie_id = request.POST['votemovie']
   
        vote.save()

        return redirect('home')



            





    
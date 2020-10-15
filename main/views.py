from django.shortcuts import render
import requests

API_KEY = "1YJNU2R902583045L4Z6"
BASE_URL = f"http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2&ServiceKey={API_KEY}"

# Create your views here.


def home(request):
    return render(request, "home.html")


def comment(request):
    return render(request, "comment.html")


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

            # 제목 단위로 검색.
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

                search_list.append(tmp_obj)

    return render(request, "comment.html", {"search_list": search_list, "search_cnt": search_cnt})

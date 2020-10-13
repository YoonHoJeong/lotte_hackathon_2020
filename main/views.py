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
    if request.method == "GET":
        # print(request)

        query = request.GET['query']
        if query:
            res = requests.get(BASE_URL + f"&query={query}").json()
            result_list = res['Data'][0]['Result']
            for movie in result_list:
                tmp_obj = {}
                title = movie['title']
                title.replace("!HS", "").replace("!HE", "")
                tmp_obj['title'] = title.strip()
                tmp_obj['plot'] = movie["plots"]['plot'][0]['plotText']
                tmp_obj['genre'] = movie["genre"]
                tmp_obj['runtime'] = movie["runtime"]
                tmp_obj['poster'] = movie['posters']
                search_list.append(tmp_obj)

            search_cnt = res['TotalCount']

    return render(request, "comment.html", {"search_list": search_list, "search_cnt": search_cnt})

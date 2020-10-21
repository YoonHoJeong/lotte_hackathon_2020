"""lotte_hackathon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from main.views import home, comment, search, movie, vote, enroll_movie, enroll_movie_search

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('comment/', comment, name="comment"),
    path('search/', search, name="search"),
    path('', include('accounts.urls')),
    path('movie/', movie, name = 'movie'),
    path('vote/', vote, name='vote'),
    path('enroll_movie/', enroll_movie, name='enroll_movie'),
    path('enroll_movie_search/', enroll_movie_search, name='enroll_movie_search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

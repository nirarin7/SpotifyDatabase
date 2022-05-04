"""SpotifyStats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path

from WebApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.log_in, name='log_in'),
    path('login/sign_in', views.sign_in, name='sign_in'),
    path('login/sign_out', views.sign_out, name='sign_out'),
    path('login/create_account_page', views.create_account_page, name='create_account_page'),
    path('login/create_account', views.create_account, name='create_account'),
    path('get_top_by_country', views.get_top_by_country, name='get_top_by_country'),
    path('get_top_genre_by_country', views.get_top_genre_by_country, name='get_top_genre_by_country'),
    path('get_top_artist_by_country', views.get_top_artist_by_country, name='get_top_artist_by_country'),
    path('get_most_danceable_songs', views.get_most_danceable_songs, name='get_most_danceable_songs'),

    path('', views.index, name='index'),
]

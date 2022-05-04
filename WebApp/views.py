from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from WebApp.models import *
from django.db import connection


# from django.core import serializers
# from django.http import HttpResponse
# from django.http import JsonResponse


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect(log_in)

    context = {
        'username': request.user.username,
    }

    return render(request, 'home/index.html', context)


def log_in(request):
    context = {}
    return render(request, 'login/login.html', context)


def sign_in(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'home/index.html', {'username': username})
        else:
            messages.error(request, "Invalid Credentials")
            return redirect(log_in)


def sign_out(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect(log_in)


def create_account_page(request):
    return render(request, 'login/create_account.html')


def create_account(request):
    if request.method == "POST":
        username = request.POST["username"]
        emailAddress = request.POST["emailAddress"]
        password = request.POST["password"]

        if User.objects.filter(username=username).first() is not None:
            messages.error(request, "Username is already taken.")
            return render(request, 'login/create_account.html')

        user = User.objects.create_user(username, emailAddress, password)
        user.save()
        messages.success(request, "Your account has successfully been created.")
        return redirect(log_in)

    return render(request, 'login/create_account.html')


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_top_by_country(request):
    if not request.user.is_authenticated:
        return redirect(log_in)

    countries = Country.objects.all().only('country')
    default = countries.filter(country='global').first()

    query = """
        select top """ + request.POST.get('count', '50') + """
            c.country as country,
            t.title as song_title,
            t.release_date as release_date,
            a.name as album,
            g.genre_type as genre,
            art.artist as artist,
            t.energy as energy,
            p.popularity as popularity

        from track t
            join album a on a.album_id = t.album_id
            join artist art on art.artist_id = a.artist_id
            join popularity p on p.track_id = t.uri
            join country c on c.country_id = p.country_id
            join genre g on g.genre_id = t.genre_id
        where c.country_id = '""" + request.POST.get('country',
                                                     str(default.country_id)) + '\' order by p.popularity desc'

    with connection.cursor() as cursor:
        cursor.execute(query)
        songs = dictfetchall(cursor)

    context = {
        'countries': countries,
        'songs': songs,
        'username': request.user.username,
        'current_country': int(request.POST.get('country', default.country_id)),
        'counts': count_dict(),
        'current_count': int(request.POST.get('count', 50))
    }
    return render(request, 'tables/top_songs_by_country.html', context)


def get_top_genre_by_country(request):
    if not request.user.is_authenticated:
        return redirect(log_in)

    countries = Country.objects.all().only('country')
    default = countries.filter(country='global').first()

    query = """
        select top """ + request.POST.get('count', '50') + """ 
            c.country as country, 
            g.genre_type as genre,
            SUM(p.popularity) as popularity
        from track t
            join popularity p on p.track_id = t.uri
            join country c on c.country_id = p.country_id
            join genre g on g.genre_id = t.genre_id
        where c.country_id = '""" + request.POST.get('country', str(default.country_id)) + """'
        group by c.country, g.genre_type
        order by SUM(p.popularity) desc
        """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = dictfetchall(cursor)
    print(rows)

    context = {
        'countries': countries,
        'rows': rows,
        'username': request.user.username,
        'current_country': int(request.POST.get('country', default.country_id)),
        'counts': count_dict(),
        'current_count': int(request.POST.get('count', 50))
    }
    return render(request, 'tables/top_genre_by_country.html', context)


def get_top_artist_by_country(request):
    if not request.user.is_authenticated:
        return redirect(log_in)

    countries = Country.objects.all().only('country')
    default = countries.filter(country='global').first()

    query = """
    SELECT top """ + request.POST.get('count', '50') + """ 
	    c.country as country, 
	    a.artist as artist,
	    SUM(p.popularity) as popularity
    from track t
        join popularity p on p.track_id = t.uri
        join country c on c.country_id = p.country_id
        join album b on b.album_id = t.album_id
        join artist a on b.artist_id = a.artist_id
    where c.country_id = '""" + request.POST.get('country', str(default.country_id)) + """'
    group by c.country, a.artist
    order by SUM(p.popularity) desc
        """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = dictfetchall(cursor)
    print(rows)

    context = {
        'countries': countries,
        'rows': rows,
        'username': request.user.username,
        'current_country': int(request.POST.get('country', default.country_id)),
        'counts': count_dict(),
        'current_count': int(request.POST.get('count', 50))
    }
    return render(request, 'tables/top_artists_by_country.html', context)


def get_most_danceable_songs(request):
    if not request.user.is_authenticated:
        return redirect(log_in)

    countries = Country.objects.all().only('country')
    default = countries.filter(country='global').first()

    query = """
    SELECT top """ + request.POST.get('count', '50') + """
        c.country AS country, 
        t.release_date AS release_date,
        a.name AS album,
        t.title AS song_title,
        g.genre_type AS genre,
        art.artist AS artist,
        t.danceability AS danceability

    FROM track t
        join album a ON a.album_id = t.album_id
        join artist art ON art.artist_id = a.artist_id
        join popularity p ON p.track_id = t.uri
        join country c ON c.country_id = p.country_id
        join genre g ON g.genre_id = t.genre_id
    WHERE country = 'Global'
    ORDER BY t.danceability DESC
        """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = dictfetchall(cursor)
    print(rows)

    context = {
        'countries': countries,
        'rows': rows,
        'username': request.user.username,
        'current_country': int(request.POST.get('country', default.country_id)),
        'counts': count_dict(),
        'current_count': int(request.POST.get('count', 50))
    }
    return render(request, 'tables/most_danceable_songs.html', context)


def count_dict():
    count = [{
            'value': 25
        }, {
            'value': 50
        }, {
            'value': 100
        }, {
            'value': 500
        }]

    return count

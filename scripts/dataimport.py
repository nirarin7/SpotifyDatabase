import csv
from datetime import datetime

from WebApp.models import *


def run():
    date_format = '%m/%d/%Y'
    with open('scripts/Spotify_Database.csv', encoding='utf8') as file:
        reader = csv.reader(file)
        next(reader)

        Album.objects.all().delete()
        Artist.objects.all().delete()
        Track.objects.all().delete()
        Country.objects.all().delete()
        Popularity.objects.all().delete()
        Genre.objects.all().delete()

        count = 0
        for row in reader:
            genre, _ = Genre.objects.get_or_create(genre_type=row[6])
            country, _ = Country.objects.get_or_create(country=row[0])

            if row[7] == '':
                followers = 0
            else:
                followers = int(row[7])

            artist, _ = Artist.objects.get_or_create(artist=row[4], followers=followers)

            album, _ = Album.objects.get_or_create(
                artist=artist,
                name=row[9],
                tracks_in_album=row[12]
            )

            try:
                release_date = datetime.strptime(row[10], date_format)
            except ValueError:
                try:
                    release_date = datetime.strptime(row[10], '%Y')
                except ValueError:
                    release_date=datetime.today()

            track, _ = Track.objects.get_or_create(
                uri=row[1],
                title=row[3],
                release_date=release_date,
                danceability=float(row[13]),
                energy=float(row[14]),
                key=int(row[15]),
                loudness=float(row[16]),
                mode=bool(row[17]),
                speechiness=float(row[18]),
                acoustics=float(row[19]),
                instrumentalness=float(row[20]),
                liveness=float(row[21]),
                valence=float(row[22]),
                tempo=float(row[23]),
                duration=int(row[24]),
                track_number_album=int(row[11]),
                album=album,
                genre=genre,
            )

            popularity, _ = Popularity.objects.get_or_create(
                country=country,
                track=track,
                popularity=float(row[2])
            )

        print("Number of rows imported: " + str(count))
